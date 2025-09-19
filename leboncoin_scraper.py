#!/usr/bin/env python3
"""
Scraper Leboncoin pour les annonces "Bureaux et commerces"
Basé sur la bibliothèque lbc d'etienne-hd
"""

import lbc
import pandas as pd
import csv
import os
from datetime import datetime
from typing import List, Optional, Dict, Any
import argparse
import json
import time
import logging

os.makedirs('logs', exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class LeboncoinBureauScraper:
    """
    Scraper pour les annonces de bureaux et commerces sur Leboncoin
    """
    
    def __init__(self, proxy=None, delay_between_requests=1):
        """
        Initialise le scraper
        
        Args:
            proxy: Configuration proxy optionnelle (str ou lbc.Proxy)
            delay_between_requests: Délai en secondes entre les requêtes
        """
        if proxy and isinstance(proxy, str):
            import re
            match = re.match(r'^http[s]?://(?:[^:@]+?:[^:@]+?@)?([^:/]+):(\d+)', proxy)
            if match:
                host = match.group(1)
                port = int(match.group(2))
                proxy = lbc.Proxy(host, port)
            else:
                raise ValueError(f"Format de proxy non reconnu : {proxy}")
        self.client = lbc.Client(proxy=proxy)
        self.delay = delay_between_requests
        self.scraped_data = []
        
    def search_bureaux_commerces(
        self,
        text: Optional[str] = None,
        locations: Optional[List] = None,
        price_range: Optional[List[int]] = None,
        surface_range: Optional[List[int]] = None,
        sort: lbc.Sort = lbc.Sort.NEWEST,
        owner_type: lbc.OwnerType = lbc.OwnerType.ALL,
        max_pages: int = 10,
        ads_per_page: int = 35,
        search_in_title_only: bool = False,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """
        Recherche des annonces de bureaux et commerces
        
        Args:
            text: Terme de recherche
            locations: Liste des localisations (City, Department, Region)
            price_range: Fourchette de prix [min, max]
            surface_range: Fourchette de surface [min, max]
            sort: Méthode de tri
            owner_type: Type de propriétaire (pro, particulier, tous)
            max_pages: Nombre maximum de pages à scraper
            ads_per_page: Nombre d'annonces par page
            search_in_title_only: Rechercher uniquement dans le titre
            **kwargs: Autres filtres spécifiques
            
        Returns:
            Liste des annonces trouvées
        """
        all_ads = []
        page = 1
        
        logger.info(f"Début du scraping pour les bureaux et commerces")
        logger.info(f"Paramètres: text='{text}', locations={len(locations) if locations else 0}, "
                   f"price_range={price_range}, surface_range={surface_range}")
        
        try:
            while page <= max_pages:
                logger.info(f"Scraping page {page}/{max_pages}")
                
                search_params = {
                    'text': text,
                    'category': lbc.Category.IMMOBILIER_BUREAUX_ET_COMMERCES,
                    'locations': locations,
                    'page': page,
                    'limit': ads_per_page,
                    'sort': sort,
                    'ad_type': lbc.AdType.OFFER,
                    'owner_type': owner_type,
                    'search_in_title_only': search_in_title_only
                }
                
                if price_range:
                    search_params['price'] = price_range
                if surface_range:
                    search_params['square'] = surface_range
                
                search_params.update(kwargs)
                
                result = self.client.search(**search_params)
                
                if not result.ads:
                    logger.info(f"Aucune annonce trouvée à la page {page}, arrêt du scraping")
                    break
                
                logger.info(f"Trouvé {len(result.ads)} annonces à la page {page}")
                
                for ad in result.ads:
                    ad_data = self._process_ad(ad)
                    all_ads.append(ad_data)
                
                if page >= result.max_pages:
                    logger.info(f"Dernière page atteinte ({result.max_pages})")
                    break
                
                page += 1
                
                if self.delay > 0:
                    time.sleep(self.delay)
                    
        except Exception as e:
            logger.error(f"Erreur lors du scraping: {e}")
            raise
        
        logger.info(f"Scraping terminé. Total: {len(all_ads)} annonces")
        self.scraped_data = all_ads
        return all_ads
    
    def _process_ad(self, ad) -> Dict[str, Any]:
        """
        Traite une annonce individuelle pour extraire les données pertinentes
        
        Args:
            ad: Objet annonce de la bibliothèque lbc
            
        Returns:
            Dictionnaire avec les données de l'annonce
        """
        try:
            attributes = {}
            for attr in ad.attributes:
                if attr.key and attr.value:
                    attributes[attr.key] = {
                        'value': attr.value,
                        'label': attr.value_label if attr.value_label else attr.value
                    }
            
            ad_data = {
                'id': ad.id,
                'title': ad.subject,
                'description': ad.body[:500] if ad.body else '',  # Limite à 500 caractères
                'price': ad.price,
                'url': ad.url,
                'publication_date': ad.first_publication_date,
                'expiration_date': ad.expiration_date,
                'category': ad.category_name,
                'status': ad.status,
                'favorites': getattr(ad, 'favorites', 0),
                
                # Localisation
                'city': ad.location.city if ad.location else '',
                'zipcode': ad.location.zipcode if ad.location else '',
                'department': ad.location.department_name if ad.location else '',
                'region': ad.location.region_name if ad.location else '',
                'latitude': ad.location.lat if ad.location else None,
                'longitude': ad.location.lng if ad.location else None,
                
                # Informations sur le vendeur
                'seller_type': 'pro' if ad.user and getattr(ad.user, 'is_pro', False) else 'particulier',
                'seller_name': ad.user.name if ad.user else '',
                'has_phone': ad.has_phone,
                
                # Images
                'images_count': len(ad.images) if ad.images else 0,
                'first_image_url': ad.images[0] if ad.images else '',
                
                # Attributs spécifiques immobilier
                'surface': self._extract_surface(attributes),
                'real_estate_type': self._extract_real_estate_type(attributes),
                'energy_class': self._extract_energy_class(attributes),
                'ges': self._extract_ges(attributes),
                'furnished': self._extract_furnished_status(attributes),
                
                # Données brutes des attributs pour analyse ultérieure
                'raw_attributes': json.dumps(attributes, ensure_ascii=False),
                
                # Métadonnées
                'scraped_at': datetime.now().isoformat()
            }
            
            if ad.user and hasattr(ad.user, 'pro') and ad.user.pro:
                pro = ad.user.pro
                ad_data.update({
                    'pro_store_name': pro.online_store_name if hasattr(pro, 'online_store_name') else '',
                    'pro_siret': pro.siret if hasattr(pro, 'siret') else '',
                    'pro_siren': pro.siren if hasattr(pro, 'siren') else '',
                    'pro_activity_sector': pro.activity_sector if hasattr(pro, 'activity_sector') else '',
                    'pro_website': pro.website_url if hasattr(pro, 'website_url') else ''
                })
            
            return ad_data
            
        except Exception as e:
            logger.error(f"Erreur lors du traitement de l'annonce {ad.id}: {e}")
            return {'id': ad.id, 'error': str(e)}
    
    def _extract_surface(self, attributes: Dict) -> Optional[int]:
        """Extrait la surface de l'annonce"""
        surface_keys = ['square', 'surface', 'area']
        for key in surface_keys:
            if key in attributes:
                try:
                    value = attributes[key]['value']
                    import re
                    match = re.search(r'\d+', str(value))
                    if match:
                        return int(match.group())
                except:
                    continue
        return None
    
    def _extract_real_estate_type(self, attributes: Dict) -> str:
        """Extrait le type de bien immobilier"""
        type_keys = ['real_estate_type', 'property_type', 'type']
        for key in type_keys:
            if key in attributes:
                return attributes[key]['label']
        return ''
    
    def _extract_energy_class(self, attributes: Dict) -> str:
        """Extrait la classe énergétique"""
        energy_keys = ['energy_rate', 'dpe', 'energy_class']
        for key in energy_keys:
            if key in attributes:
                return attributes[key]['label']
        return ''
    
    def _extract_ges(self, attributes: Dict) -> str:
        """Extrait les émissions GES"""
        ges_keys = ['ges', 'greenhouse_gas', 'co2']
        for key in ges_keys:
            if key in attributes:
                return attributes[key]['label']
        return ''
    
    def _extract_furnished_status(self, attributes: Dict) -> str:
        """Extrait le statut meublé/non meublé"""
        furnished_keys = ['furnished', 'meuble', 'furnished_type']
        for key in furnished_keys:
            if key in attributes:
                return attributes[key]['label']
        return ''
    
    def save_to_csv(self, filename: str = None, city: str = None, include_raw_attributes: bool = False) -> str:
        """
        Sauvegarde les données en CSV
        
        Args:
            filename: Nom du fichier (optionnel)
            include_raw_attributes: Inclure les attributs bruts
            
        Returns:
            Nom du fichier créé
        """
        if not self.scraped_data:
            raise ValueError("Aucune donnée à sauvegarder. Exécutez d'abord une recherche.")
        
        data_dir = "data"
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            city_part = city if city else "all"
            filename = f"leboncoin_bureaux_commerces_{city_part}_{timestamp}.csv"
        
        if not filename.startswith(data_dir):
            filename = os.path.join(data_dir, filename)
        
        csv_data = []
        for ad in self.scraped_data:
            if 'error' in ad:
                continue
            
            csv_row = ad.copy()
            
            if not include_raw_attributes:
                csv_row.pop('raw_attributes', None)
            
            csv_data.append(csv_row)
        
        df = pd.DataFrame(csv_data)
        
        df.to_csv(filename, index=False, encoding='utf-8')
        logger.info(f"Données sauvegardées dans {filename} ({len(csv_data)} annonces)")
        
        return filename
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Génère des statistiques sur les données scrapées
        
        Returns:
            Dictionnaire avec les statistiques
        """
        if not self.scraped_data:
            return {}
        
        df = pd.DataFrame(self.scraped_data)
        
        stats = {
            'total_ads': len(df),
            'unique_cities': df['city'].nunique() if 'city' in df.columns else 0,
            'price_stats': {
                'mean': df['price'].mean() if 'price' in df.columns else 0,
                'median': df['price'].median() if 'price' in df.columns else 0,
                'min': df['price'].min() if 'price' in df.columns else 0,
                'max': df['price'].max() if 'price' in df.columns else 0
            },
            'seller_types': df['seller_type'].value_counts().to_dict() if 'seller_type' in df.columns else {},
            'top_cities': df['city'].value_counts().head(10).to_dict() if 'city' in df.columns else {}
        }
        
        return stats


def main():
    """Fonction principale pour l'utilisation en ligne de commande"""
    parser = argparse.ArgumentParser(description='Scraper Leboncoin - Bureaux et commerces')
    
    parser.add_argument('--text', type=str, help='Terme de recherche')
    parser.add_argument('--city', type=str, help='Ville de recherche')
    parser.add_argument('--lat', type=float, help='Latitude')
    parser.add_argument('--lng', type=float, help='Longitude')
    parser.add_argument('--radius', type=int, default=10000, help='Rayon de recherche en mètres')
    parser.add_argument('--min-price', type=int, help='Prix minimum')
    parser.add_argument('--max-price', type=int, help='Prix maximum')
    parser.add_argument('--min-surface', type=int, help='Surface minimum')
    parser.add_argument('--max-surface', type=int, help='Surface maximum')
    parser.add_argument('--max-pages', type=int, default=5, help='Nombre maximum de pages à scraper')
    parser.add_argument('--output', type=str, help='Nom du fichier de sortie CSV')
    parser.add_argument('--delay', type=float, default=3.0, help='Délai entre les requêtes')
    parser.add_argument('--owner-type', choices=['pro', 'private', 'all'], default='all', help='Type de vendeur')
    parser.add_argument('--stats', action='store_true', help='Afficher les statistiques')
    parser.add_argument('--proxy', type=str, help='Proxy HTTP/HTTPS (ex: http://user:pass@host:port)', default=None)
    
    args = parser.parse_args()
    
    locations = []
    if args.city and args.lat and args.lng:
        location = lbc.City(
            lat=args.lat,
            lng=args.lng,
            radius=args.radius,
            city=args.city
        )
        locations = [location]
    
    price_range = None
    if args.min_price and args.max_price:
        price_range = [args.min_price, args.max_price]
    
    surface_range = None
    if args.min_surface and args.max_surface:
        surface_range = [args.min_surface, args.max_surface]
    
    owner_type_map = {
        'pro': lbc.OwnerType.PRO,
        'private': lbc.OwnerType.PRIVATE,
        'all': lbc.OwnerType.ALL
    }
    owner_type = owner_type_map[args.owner_type]
    
    scraper = LeboncoinBureauScraper(delay_between_requests=args.delay, proxy=args.proxy)
    
    try:
        ads = scraper.search_bureaux_commerces(
            text=args.text,
            locations=locations,
            price_range=price_range,
            surface_range=surface_range,
            max_pages=args.max_pages,
            owner_type=owner_type
        )
        
        if ads:
            filename = scraper.save_to_csv(args.output, city=args.city)
            print(f"Données sauvegardées dans: {filename}")
            
            if args.stats:
                stats = scraper.get_statistics()
                print("\n=== STATISTIQUES ===")
                print(f"Nombre total d'annonces: {stats['total_ads']}")
                print(f"Villes uniques: {stats['unique_cities']}")
                print(f"Prix moyen: {stats['price_stats']['mean']:.2f}€")
                print(f"Prix médian: {stats['price_stats']['median']:.2f}€")
                print(f"Répartition vendeurs: {stats['seller_types']}")
                print(f"Top 5 villes: {dict(list(stats['top_cities'].items())[:5])}")
        else:
            print("Aucune annonce trouvée avec ces critères.")
            
    except Exception as e:
        logger.error(f"Erreur: {e}")
        print(f"Erreur lors du scraping: {e}")


if __name__ == "__main__":
    main()