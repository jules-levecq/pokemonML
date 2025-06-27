#!/usr/bin/env python3
# main.py

from pokemonml.create_pokemon import PokemonFactory
from pokemonml.damage import PokemonDamageCalculator
from pokemonml.right_move_machine import RightMoveMachine
from pokemonml.display import display_turn_summary
from pokemonml.config import POKEMON_CSV, MOVES_CSV, TYPE_CHART_CSV
from pokemonml.team import Team

# ================================
#  SETUP: Initialize all systems
# ================================

# On récupère les chemins depuis config.py
factory = PokemonFactory(POKEMON_CSV, MOVES_CSV)
damage_calculator = PokemonDamageCalculator(TYPE_CHART_CSV, verbose=False)
right_move_machine = RightMoveMachine(verbose=False)

# Create and configure Pokémon
pikachu = factory.create_pokemon("Pikachu",   50)
alakazam = factory.create_pokemon("Alakazam", 50)
charizard = factory.create_pokemon("Charizard", 50)
snorlax = factory.create_pokemon("Snorlax", 50)
gyarados = factory.create_pokemon("Gyarados", 50)
machamp = factory.create_pokemon("Machamp", 50)

# Assign moves to Pokémon
for move_name in ["Thunder", "Quick Attack", "Iron Tail", "Volt Tackle"]:
    factory.add_move_to_pokemon(pikachu, move_name)

# Create a list of pokemon to simulate teams
team1 = Team([pikachu, charizard, snorlax], name="Player")
team2 = Team([alakazam, gyarados, machamp], name="Bot")

while not team1.is_defeated() and not team2.is_defeated():
    active1 = team1.active_pokemon
    active2 = team2.active_pokemon
    # phase de choix d'action...
    # team1.switch_to(2) par exemple


# ================================
#  TURN EXECUTION
# ================================

# 1. Prédiction du meilleur coup
predicted_attack = right_move_machine.find_best_move(pikachu, alakazam)

# 2. Exécution réelle du coup (sans hasard pour être reproductible)
executed_attack = damage_calculator.resolve_interaction(
    attacker=pikachu,
    defender=alakazam,
    move=predicted_attack.move,
    random_multiplier=False
)

# 3. Affichage du résumé du tour
display_turn_summary(pikachu, alakazam, predicted_attack, executed_attack)
