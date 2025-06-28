#!/usr/bin/env python3
# main.py
import random

from pokemonml.create_pokemon import PokemonFactory
from pokemonml.damage import PokemonDamageCalculator
from pokemonml.right_move_machine import RightMoveMachine
from pokemonml.display import display_turn_summary
from pokemonml.config import POKEMON_CSV, MOVES_CSV, TYPE_CHART_CSV
from pokemonml.team import Team
from random import randint

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

# Assign moves to Pokémon
for move_name in ["Thunder", "Quick Attack", "Iron Tail", "Volt Tackle"]:
    factory.add_move_to_pokemon(pikachu, move_name)
factory.add_move_to_pokemon(alakazam, "Thunder")

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
