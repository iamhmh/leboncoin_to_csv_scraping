# Leboncoin Scraper (Bureaux et commerces)

Un scraper en ligne de commande pour extraire les annonces de "Bureaux et commerces" sur Leboncoin, basé sur la bibliothèque [lbc](https://github.com/etienne-hd/lbc).

## ✨ Points clés
- Une seule commande à exécuter: `lbc-scrape`
- Export CSV automatique dans `data/`
- Logs propres dans `logs/scraper.log`
- Options simples en CLI (+ API Python optionnelle)

## 🚀 Installation rapide
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```
La dernière ligne installe la commande `lbc-scrape` dans votre environnement.

## 🏃 Utilisation en une ligne
```bash
# Recherche simple (3 pages) de bureaux à Paris
lbc-scrape --text "bureau" --city "Paris" --lat 48.8566 --lng 2.3522 --max-pages 3

# Avec filtres de prix et surface
lbc-scrape --text "local commercial" --city "Lyon" --lat 45.7640 --lng 4.8357 \
    --min-price 1000 --max-price 5000 --min-surface 50 --max-surface 200

# Pros uniquement + statistiques + nom de fichier
lbc-scrape --text "commerce" --city "Marseille" --lat 43.2965 --lng 5.3698 \
    --owner-type pro --stats --output "marseille_pro.csv"
```
Tous les CSV sont automatiquement enregistrés dans `data/`.

## 🛠️ Options principales
| Argument | Description | Exemple |
|----------|-------------|---------|
| `--text` | Terme de recherche | `--text "bureau"` |
| `--city` | Ville | `--city "Paris"` |
| `--lat` / `--lng` | Coordonnées GPS | `--lat 48.8566 --lng 2.3522` |
| `--radius` | Rayon (mètres) | `--radius 20000` |
| `--min-price` / `--max-price` | Fourchette de prix | `--min-price 500 --max-price 3000` |
| `--min-surface` / `--max-surface` | Fourchette de surface | `--min-surface 20 --max-surface 200` |
| `--max-pages` | Pages max | `--max-pages 10` |
| `--owner-type` | Vendeur (`pro`, `private`, `all`) | `--owner-type pro` |
| `--delay` | Délai entre requêtes (s) | `--delay 2.0` |
| `--output` | Nom du CSV (dans `data/`) | `--output "resultats.csv"` |
| `--stats` | Afficher les stats | `--stats` |

## 🧪 API Python (optionnel)
```python
from leboncoin_scraper import LeboncoinBureauScraper
import lbc

scraper = LeboncoinBureauScraper(delay_between_requests=1.0)
paris = lbc.City(lat=48.8566, lng=2.3522, radius=15000, city="Paris")
ads = scraper.search_bureaux_commerces(text="bureau", locations=[paris], max_pages=3)
filename = scraper.save_to_csv("bureaux_paris.csv")  # => data/bureaux_paris.csv
print(filename)
```

## 🐛 Dépannage
- Activez votre venv: `source .venv/bin/activate`
- Réinstallez: `pip install -r requirements.txt`
- Consultez les logs: `logs/scraper.log`
- Réduisez `--max-pages` ou augmentez `--delay` si nécessaire

## ⚖️ Respect et conditions
Projet non affilié à Leboncoin. Respectez leurs conditions d’utilisation.

## Licence 
Ce projet est sous licence MIT License.