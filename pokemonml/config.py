from pathlib import Path

# Répertoire racine du projet (deux niveaux depuis ce fichier)
BASE_DIR = Path(__file__).resolve().parent.parent

# Dossier contenant les CSV de données
DATA_DIR = BASE_DIR / 'data'

# Fichiers de données externes
POKEMON_CSV    = DATA_DIR / 'pokemon.csv'
MOVES_CSV      = DATA_DIR / 'moves.csv'
NATURES_CSV    = DATA_DIR / 'natures.csv'
TYPE_CHART_CSV = DATA_DIR / 'chart.csv'
