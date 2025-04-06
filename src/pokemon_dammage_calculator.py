from .data_loader import read_csv_data
import random


class PokemonDamageCalculator:
    """
    A class to calculate the damage to a Pokémon move based on type effectiveness
    and combat statistics.
    """

    def __init__(self, csv_path):
        """
        Load the type effectiveness chart from a CSV file.

        :param csv_path: Path to the type effectiveness chart CSV.
        """
        type_chart_df = read_csv_data(csv_path)
        type_chart_df.set_index('Attacking', inplace=True)
        self.type_chart = type_chart_df

    def get_effectiveness(self, attack_type, defender_type):
        """
        Get the effectiveness multiplier for a move type against a defender's type.

        :param attack_type: Type of the attack (e.g., "Electric")
        :param defender_type: Defender's type (e.g., "Water")
        :return: Multiplier as a float (e.g., 0.5, 1.0, 2.0)
        """
        return self.type_chart.loc[attack_type, defender_type]

    def calculate_damage(self, attacker, defender, move):
        """
        Calculate the damage inflicted by a move from attacker to defender.

        :param attacker: Pokémon performing the attack
        :param defender: Pokémon receiving the attack
        :param move: Move object being used
        :return: Calculated damage as a float
        """
        # Check if the move hits
        hit_chance = random.uniform(0, 100)
        if hit_chance > move.accuracy:
            print(f"{attacker.name}'s {move.name} missed!")
            return 0.0

        # Choose the relevant stats based on the move's category
        if move.damage_class == 'physical':
            attack_stat = attacker.stats.attack
            defense_stat = defender.stats.defense
        else:
            attack_stat = attacker.stats.attack_spe
            defense_stat = defender.stats.defense_spe

        # Basic damage formula
        base_damage = (((2 * attacker.level / 5 + 2) * move.damage * (attack_stat / defense_stat)) / 50) + 2

        # Apply STAB (Same-Type Attack Bonus)
        if move.element == attacker.type1 or move.element == attacker.type2:
            base_damage *= 1.5

        # Calculate effectiveness based on defender's types
        effectiveness = self.get_effectiveness(move.element, defender.type1)
        if defender.type2:
            effectiveness *= self.get_effectiveness(move.element, defender.type2)

        print(f"Effectiveness of {move.element} against {defender.type1}/{defender.type2 or 'None'}: {effectiveness}")

        return base_damage * effectiveness
