from src.data_loader import read_csv_data
from src.create_pokemon import PokemonFactory
from src.pokemon_dammage_calculator import PokemonDamageCalculator

# Initialisation de la factory et du calculateur
factory = PokemonFactory('data/pokemon.csv', 'data/moves.csv')
damage_calculator = PokemonDamageCalculator('data/chart.csv')

# Création des Pokémon
pikachu = factory.create_pokemon("Pikachu")
bulbasaur = factory.create_pokemon("Bulbasaur")

# Ajout des attaques
factory.add_move_to_pokemon(pikachu, "Thunderbolt")
factory.add_move_to_pokemon(bulbasaur, "Vine Whip")

# Calcul des dégâts
damage = damage_calculator.calculate_damage(pikachu, bulbasaur, pikachu.moves[0])

# Affichage
print(f"{pikachu.name} inflige {damage:.2f} dégâts à {bulbasaur.name} avec l'attaque {pikachu.moves[0].name}.")
