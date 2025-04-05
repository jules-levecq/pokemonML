from src import data_loader as dl
from src import pokemon_dammage_calculator as pdc
from src import create_pokemon as cp

# Chargement des données
pokemon_data = dl.read_csv_data('data/Pokemon.csv')
moves_data = dl.read_csv_data('data/moves.csv')

# Création des Pokémon
pikachu = cp.create_pokemon("Pikachu", pokemon_data)
bulbasaur = cp.create_pokemon("Bulbasaur", pokemon_data)

# Création des attaques
thunderbolt = cp.create_move("Thunderbolt", moves_data)
vine_whip = cp.create_move("Vine Whip", moves_data)

# Attribution des attaques aux Pokémon
cp.add_move_to_pokemon(pikachu, thunderbolt)
cp.add_move_to_pokemon(bulbasaur, vine_whip)

# Initialisation du calculateur de dégâts
damage_calculator = pdc.PokemonDamageCalculator('data/chart.csv')

# Calcul des dégâts infligés par Pikachu à Bulbasaur
damage = damage_calculator.calculate_damage(pikachu, bulbasaur, pikachu.moves[0])

# Affichage des résultats
print(f"{pikachu.name} inflige {damage:.2f} dégâts à {bulbasaur.name} avec l'attaque {pikachu.moves[0].name}.")
