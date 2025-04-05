from .data_loader import read_csv_data


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

    def calculate_damage(self, attacker, defender, move):
        if move.damage_class == 'Physical':
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
    def __init__(self, name, element, damage, damage_class, accuracy):
        self.name = name
        self.element = element
        self.damage = damage
        self.damage_class = damage_class
        self.accuracy = accuracy
