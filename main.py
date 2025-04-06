from src.create_pokemon import PokemonFactory
from src.pokemon_dammage_calculator import PokemonDamageCalculator

# Initialize the factory and the damage calculator
factory = PokemonFactory('data/pokemon.csv', 'data/moves.csv')
damage_calculator = PokemonDamageCalculator('data/chart.csv')

# Create Pokémon
pikachu = factory.create_pokemon("Pikachu")
bulbasaur = factory.create_pokemon("Bulbasaur")

# Add moves
factory.add_move_to_pokemon(pikachu, "Thunderbolt")
factory.add_move_to_pokemon(bulbasaur, "Vine Whip")

# Calculate damage
damage = damage_calculator.calculate_damage(pikachu, bulbasaur, pikachu.moves[0])

# Display the result
print(f"{pikachu.name} deals {damage:.2f} damage to {bulbasaur.name} using {pikachu.moves[0].name}.")
