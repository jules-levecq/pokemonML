# team_builder.py

import json
from pathlib import Path
import pandas as pd
from pokemonml.config import POKEMON_CSV, MOVES_CSV

TEAMS_FILE = Path('teams.json')

def load_pokemon_list():
    """Retourne la liste des noms de Pokémon disponibles."""
    df = pd.read_csv(POKEMON_CSV)
    return df['name'].tolist()

def load_moves_list():
    """Retourne la liste des noms de Moves disponibles."""
    df = pd.read_csv(MOVES_CSV)
    return df['name'].tolist()

def load_teams():
    """Charge le dict des équipes depuis teams.json."""
    if TEAMS_FILE.exists():
        return json.loads(TEAMS_FILE.read_text(encoding='utf-8'))
    return {}

def save_teams(teams: dict):
    """Écrit le dict des équipes dans teams.json."""
    TEAMS_FILE.write_text(json.dumps(teams, ensure_ascii=False, indent=2), encoding='utf-8')

def add_team(name: str, members: list):
    """Ajoute ou remplace une équipe nommée."""
    teams = load_teams()
    teams[name] = members
    save_teams(teams)

def delete_team(name: str):
    """Supprime une équipe par son nom."""
    teams = load_teams()
    if name in teams:
        del teams[name]
        save_teams(teams)
