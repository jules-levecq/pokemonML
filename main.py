from pokemonml.create_pokemon import PokemonFactory
from pokemonml.damage import PokemonDamageCalculator
from pokemonml.right_move_machine import RightMoveMachine
from pokemonml.display import display_turn_summary

# ================================
#  SETUP: Initialize all systems
# ================================

# Load data sources and create utility managers
factory = PokemonFactory('data/pokemon.csv', 'data/moves.csv')
damage_calculator = PokemonDamageCalculator('data/chart.csv', verbose=False)
right_move_machine = RightMoveMachine('data/chart.csv', verbose=False)

# Create and configure Pokémon
pikachu = factory.create_pokemon("Pikachu", 50)
bulbasaur = factory.create_pokemon("Bulbasaur", 50)

# Assign moves to Pokémon
factory.add_move_to_pokemon(pikachu, "Thunder")
factory.add_move_to_pokemon(pikachu, "Quick Attack")
factory.add_move_to_pokemon(pikachu, "Iron Tail")
factory.add_move_to_pokemon(pikachu, "Volt Tackle")
factory.add_move_to_pokemon(bulbasaur, "Vine Whip")

# ================================
#  TURN EXECUTION
# ================================

# Step 1: Predict best move
predicted_attack = right_move_machine.find_best_move(pikachu, bulbasaur)

# Step 2: Resolve actual move execution
executed_attack = damage_calculator.resolve_interaction(
    pikachu, bulbasaur,
    move=predicted_attack.move,
    random_multiplier=False
)

# Step 3: Display result summary
display_turn_summary(pikachu, bulbasaur, predicted_attack, executed_attack)
