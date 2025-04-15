from src.create_pokemon import PokemonFactory
from src.pokemon_dammage_calculator import PokemonDamageCalculator
from src.right_move_machine import RightMoveMachine
from src.utils import display_damage_result


# Initialize the factory and the damage calculator
factory = PokemonFactory('data/pokemon.csv', 'data/moves.csv')
damage_calculator = PokemonDamageCalculator('data/chart.csv')

# Create Pokémon
pikachu = factory.create_pokemon("Pikachu", 50)
bulbasaur = factory.create_pokemon("Bulbasaur", 50)

# Add moves
factory.add_move_to_pokemon(pikachu, "Thunder")
factory.add_move_to_pokemon(pikachu, "Quick Attack")
factory.add_move_to_pokemon(pikachu, "Iron Tail")
factory.add_move_to_pokemon(pikachu, "Volt Tackle")
factory.add_move_to_pokemon(bulbasaur, "Vine Whip")

# Find the best move
best_attack = RightMoveMachine.find_best_move(pikachu, bulbasaur)
display_damage_result(pikachu, bulbasaur, best_attack.move, best_attack)

# Display the pp of best attack move
print(f"PP of the best attack move: {best_attack.move.pp}")
# Display the health of bulbasaur before the attack
print(f"Bulbasaur's health before the attack: {bulbasaur.current_stats.health}")
# Do the attack
best_attack = damage_calculator.return_interaction(pikachu, bulbasaur, best_attack.move, random_multiplier=False)
display_damage_result(pikachu, bulbasaur, best_attack.move, best_attack)
# Display the pp of best attack move
print(f"PP of the best attack move: {best_attack.move.pp}")
# Display the health of bulbasaur after the attack
print(f"Bulbasaur's health after the attack: {round(bulbasaur.current_stats.health, 2)}")
