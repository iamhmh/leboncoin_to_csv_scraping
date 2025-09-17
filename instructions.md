# Instructions pour l'agent IA de codage

## Objectif
Créer un projet de scraping performant pour extraire toutes les annonces "Bureaux & Commerces" sur Leboncoin et sauvegarder les données dans un fichier CSV bien structuré et annoté.

## Fonctionnalités attendues
1. **Scraping complet**
   - Cibler exclusivement la catégorie "Bureaux & Commerces".
   - Extraire toutes les annonces disponibles (actuellement 140 892 annonces).
   - Récupérer toutes les informations pertinentes de chaque annonce :
     - Titre
     - Description complète
     - Prix
     - Loyer (si disponible)
     - Surface (si disponible)
     - Type de bien
     - Localisation (adresse, ville, code postal, région)
     - Date de publication
     - Nom du vendeur ou professionnel
     - Contact (si accessible légalement)
     - URL de l'annonce
   
2. **Performance**
   - Scraper de manière efficace, gérer la pagination automatiquement.
   - Implémenter un système de throttling / delay pour éviter le blocage.
   - Possibilité de relancer le scraping depuis la dernière annonce récupérée.

3. **Format de sortie**
   - Générer un fichier CSV bien annoté.
   - Les colonnes doivent être claires, cohérentes et commentées si nécessaire.
   - Option : ajouter un fichier JSON complémentaire pour des données complexes (ex : liste d’images).

4. **Robustesse**
   - Gérer les erreurs de réseau, les annonces supprimées et les pages vides.
   - Logging des étapes et erreurs pour faciliter le débogage.

5. **Technologies recommandées**
   - Python (requests, BeautifulSoup / lxml, Selenium si nécessaire)
   - Pandas pour la manipulation et l’export CSV
   - Possibilité d’utiliser `asyncio` ou `aiohttp` pour le scraping asynchrone.

6. **Conformité**
   - Respecter les conditions d’utilisation de Leboncoin.
   - Ne pas saturer le site par des requêtes massives simultanées.
   
## Instructions à l’agent IA
1. Générer un projet complet avec structure claire (`scraper.py`, `utils.py`, `config.py`, etc.).
2. Écrire du code commenté et lisible, avec fonctions modulaires.
3. Prévoir un fichier `README.md` expliquant comment lancer le scraping et générer le CSV.
4. Fournir un exemple de CSV généré (avec 5-10 annonces) pour vérifier le format.
5. Écrire des tests unitaires simples pour vérifier la récupération des données.

## Priorités
1. Exactitude des données.
2. Complétude des annonces.
3. Performance et sécurité.
4. Lisibilité du code et documentation.
