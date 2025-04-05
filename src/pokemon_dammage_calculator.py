from data_loader import read_csv_data
from create_pokemon import create_pokemon, create_move, add_move_to_pokemon


class PokemonDamageCalculator:
    """Classe pour calculer les dégâts d'une attaque Pokémon en utilisant la table d'efficacité des types."""

    def __init__(self, csv_path):
        # Utilisation de ta propre fonction pour lire les données CSV
        type_chart_df = read_csv_data(csv_path)
        type_chart_df.set_index('Attacking', inplace=True)
        self.type_chart = type_chart_df

    def get_effectiveness(self, attack_type, defender_type):
        """Obtenir le multiplicateur d'efficacité selon les types."""
        return self.type_chart.loc[attack_type, defender_type]

    def calculateDamage(self, attacker, defender, move):
        if move.category == 'physical':
            attack_stat = attacker.stats.attack
            defense_stat = defender.stats.defense
        else:
            attack_stat = attacker.stats.attack_spe
            defense_stat = defender.stats.defense_spe

        base_damage = (((2 * attacker.level / 5 + 2) * move.damage * (attack_stat / defense_stat)) / 50) + 2

        # STAB (bonus de même type)
        if move.element == attacker.type1 or move.element == attacker.type2:
            base_damage *= 1.5

        # Multiplicateur d'efficacité en considérant les deux types du défenseur
        effectiveness = self.get_effectiveness(move.element, defender.type1)
        if defender.type2:
            effectiveness *= self.get_effectiveness(move.element, defender.type2)

        print(f"Efficacité de {move.element} contre {defender.type1}/{defender.type2 or 'aucun'} : {effectiveness}")

        return base_damage * effectiveness

# Classes inchangées


class Stats:
    def __init__(self, health, attack, defense, attack_spe, defense_spe, speed):
        self.health = health
        self.attack = attack
        self.defense = defense
        self.attack_spe = attack_spe
        self.defense_spe = defense_spe
        self.speed = speed

class Pokemon:
    def __init__(self, name, stats, moves, type1, type2=None, level=50):
        self.name = name
        self.stats = stats
        self.type1 = type1
        self.type2 = type2
        self.level = level
        self.moves = moves


class Move:
    def __init__(self, name, element, damage, category, accuracy):
        self.name = name
        self.element = element
        self.damage = damage
        self.category = category
        self.accuracy = accuracy

# Exemple d'utilisation
pikachu_stats = Stats(35, 55, 40, 50, 50, 90)
pikachu_moves = [Move('Thunderbolt', 'Electric', 90, 'special', 100)]
pikachu = Pokemon('Pikachu', pikachu_stats, pikachu_moves, 'Electric')

bulbasaur_stats = Stats(45, 49, 49, 65, 65, 45)
bulbasaur_moves = [Move('Vine Whip', 'Grass', 45, 'special', 100)]
bulbasaur = Pokemon('Bulbasaur', bulbasaur_stats, bulbasaur_moves, 'Grass', 'Poison')

# Création du calculateur en utilisant ta fonction pour lire les données CSV
damage_calculator = PokemonDamageCalculator('chart.csv')

# Calcul des dégâts
damage = damage_calculator.calculateDamage(pikachu, bulbasaur, pikachu.moves[0])

print(f"Dégâts infligés par {pikachu.name} avec {pikachu.moves[0].name} à {bulbasaur.name} : {damage:.2f}")




# Chargement des données
pokemon_data = read_csv_data('data/Pokemon.csv')
moves_data = read_csv_data('data/moves.csv')

# Création des Pokémon
pikachu = create_pokemon("Pikachu", pokemon_data)
bulbasaur = create_pokemon("Bulbasaur", pokemon_data)

# Création des attaques
thunderbolt = create_move("Thunderbolt", moves_data)
vine_whip = create_move("Vine Whip", moves_data)

# Attribution des attaques aux Pokémon
add_move_to_pokemon(pikachu, thunderbolt)
add_move_to_pokemon(bulbasaur, vine_whip)

# Initialisation du calculateur de dégâts
damage_calculator = PokemonDamageCalculator('data/chart.csv')

# Calcul des dégâts infligés par Pikachu à Bulbasaur
damage = damage_calculator.calculateDamage(pikachu, bulbasaur, pikachu.moves[0])

# Affichage des résultats
print(f"{pikachu.name} inflige {damage:.2f} dégâts à {bulbasaur.name} avec l'attaque {pikachu.moves[0].name}.")
