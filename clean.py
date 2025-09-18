#!/usr/bin/env python3
"""
Script de nettoyage et d'organisation des fichiers CSV
Déplace les anciens fichiers CSV vers le dossier exports/
"""

import os
import shutil
import glob
from datetime import datetime


def move_csv_files_to_exports():
    """Déplace tous les fichiers CSV du répertoire racine vers exports/"""
    
    # Créer le dossier exports s'il n'existe pas
    exports_dir = "exports"
    if not os.path.exists(exports_dir):
        os.makedirs(exports_dir)
        print(f"📁 Dossier créé : {exports_dir}/")
    
    # Trouver tous les fichiers CSV dans le répertoire racine
    csv_files = glob.glob("*.csv")
    
    if not csv_files:
        print("✅ Aucun fichier CSV à déplacer dans le répertoire racine")
        return
    
    moved_count = 0
    
    for csv_file in csv_files:
        try:
            # Vérifier si le fichier existe déjà dans exports
            destination = os.path.join(exports_dir, csv_file)
            
            if os.path.exists(destination):
                # Ajouter un timestamp pour éviter les conflits
                name, ext = os.path.splitext(csv_file)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                new_name = f"{name}_moved_{timestamp}{ext}"
                destination = os.path.join(exports_dir, new_name)
                print(f"⚠️  Fichier existant renommé : {csv_file} -> {new_name}")
            
            # Déplacer le fichier
            shutil.move(csv_file, destination)
            print(f"📦 Déplacé : {csv_file} -> {destination}")
            moved_count += 1
            
        except Exception as e:
            print(f"❌ Erreur lors du déplacement de {csv_file} : {e}")
    
    print(f"\n✅ {moved_count} fichier(s) CSV déplacé(s) vers {exports_dir}/")


def organize_log_files():
    """Organise les fichiers de log dans le dossier logs/"""
    
    logs_dir = "logs"
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
        print(f"📁 Dossier créé : {logs_dir}/")
    
    # Trouver les fichiers de log dans le répertoire racine
    log_files = glob.glob("*.log")
    
    moved_count = 0
    
    for log_file in log_files:
        try:
            destination = os.path.join(logs_dir, log_file)
            
            if os.path.exists(destination):
                # Fusionner les logs ou renommer
                name, ext = os.path.splitext(log_file)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                new_name = f"{name}_moved_{timestamp}{ext}"
                destination = os.path.join(logs_dir, new_name)
            
            shutil.move(log_file, destination)
            print(f"📋 Log déplacé : {log_file} -> {destination}")
            moved_count += 1
            
        except Exception as e:
            print(f"❌ Erreur lors du déplacement de {log_file} : {e}")
    
    if moved_count == 0:
        print("✅ Aucun fichier de log à déplacer")
    else:
        print(f"✅ {moved_count} fichier(s) de log déplacé(s)")


def clean_temp_files():
    """Supprime les fichiers temporaires et de cache"""
    
    patterns_to_clean = [
        "__pycache__/",
        "*.pyc",
        "*.pyo",
        "*.pyd",
        ".DS_Store",
        "*.tmp",
        "*.temp"
    ]
    
    cleaned_count = 0
    
    for pattern in patterns_to_clean:
        if pattern.endswith("/"):
            # Dossiers
            if os.path.exists(pattern):
                try:
                    shutil.rmtree(pattern)
                    print(f"🗑️  Dossier supprimé : {pattern}")
                    cleaned_count += 1
                except Exception as e:
                    print(f"❌ Erreur lors de la suppression de {pattern} : {e}")
        else:
            # Fichiers avec pattern
            files = glob.glob(pattern)
            for file in files:
                try:
                    os.remove(file)
                    print(f"🗑️  Fichier supprimé : {file}")
                    cleaned_count += 1
                except Exception as e:
                    print(f"❌ Erreur lors de la suppression de {file} : {e}")
    
    if cleaned_count == 0:
        print("✅ Aucun fichier temporaire à nettoyer")
    else:
        print(f"✅ {cleaned_count} fichier(s)/dossier(s) temporaire(s) nettoyé(s)")


def show_directory_structure():
    """Affiche la structure des dossiers après nettoyage"""
    
    print("\n📁 STRUCTURE DU PROJET APRÈS NETTOYAGE :")
    print("=" * 50)
    
    # Dossiers principaux
    main_dirs = ["exports", "logs", "data"]
    
    for directory in main_dirs:
        if os.path.exists(directory):
            files = os.listdir(directory)
            print(f"📂 {directory}/ ({len(files)} fichier(s))")
            
            # Afficher quelques fichiers exemple
            for file in files[:3]:
                print(f"   📄 {file}")
            
            if len(files) > 3:
                print(f"   ... et {len(files) - 3} autre(s)")
        else:
            print(f"📂 {directory}/ (vide)")
    
    # Fichiers dans le répertoire racine
    root_files = [f for f in os.listdir(".") if os.path.isfile(f) and not f.startswith(".")]
    print(f"\n📂 Répertoire racine ({len(root_files)} fichier(s))")
    
    python_files = [f for f in root_files if f.endswith('.py')]
    other_files = [f for f in root_files if not f.endswith('.py')]
    
    for file in python_files:
        print(f"   🐍 {file}")
    
    for file in other_files[:5]:  # Limite à 5 autres fichiers
        print(f"   📄 {file}")
    
    if len(other_files) > 5:
        print(f"   ... et {len(other_files) - 5} autre(s)")


def main():
    """Fonction principale de nettoyage"""
    
    print("🧹 NETTOYAGE ET ORGANISATION DU PROJET")
    print("=" * 50)
    print(f"Date : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print()
    
    # Étape 1 : Déplacer les fichiers CSV
    print("📦 Étape 1 : Organisation des fichiers CSV")
    print("-" * 30)
    move_csv_files_to_exports()
    
    # Étape 2 : Organiser les logs
    print(f"\n📋 Étape 2 : Organisation des fichiers de log")
    print("-" * 30)
    organize_log_files()
    
    # Étape 3 : Nettoyer les fichiers temporaires
    print(f"\n🧹  Étape 3 : Nettoyage des fichiers temporaires")
    print("-" * 30)
    clean_temp_files()
    
    # Étape 4 : Afficher la structure finale
    show_directory_structure()
    
    print(f"\n🎉 Nettoyage terminé ! Tous vos fichiers CSV sont maintenant dans le dossier exports/")
    print("💡 Conseil : Les nouveaux fichiers CSV seront automatiquement sauvegardés dans exports/")


if __name__ == "__main__":
    main()