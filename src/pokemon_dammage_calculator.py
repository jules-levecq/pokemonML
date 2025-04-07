import random
import copy
from dataclasses import dataclass
from .utils import read_csv_data
from .create_pokemon import Pokemon


@dataclass
class Attack:
    """
    Dataclass representing the result of a single attack calculation.
    """
    damage_range: tuple  # (min_damage, max_damage)
    effective_damage: float  # Actual damage dealt
    missed: bool  # True if the move missed
    crit: bool  # True if it was a critical hit
    effectiveness: float  # Type effectiveness multiplier
    defender: Pokemon  # Snapshot of the defender at the time of the attack
    attacker: Pokemon  # Snapshot of the attacker at the time of the attack
    move: object  # Copy of the move used


class PokemonDamageCalculator:
    """
    Class responsible for computing damage based on Pokémon stats and type effectiveness.
    """

    def __init__(self, csv_path):
        """
        Initialize the calculator by loading the type effectiveness chart.

        :param csv_path: Path to the type chart CSV file.
        """
        type_chart_df = read_csv_data(csv_path)
        type_chart_df.set_index('Attacking', inplace=True)
        self.type_chart = type_chart_df

    def get_effectiveness(self, attack_type, defender_type):
        """
        Get the type effectiveness multiplier between attack and defense type.

        :param attack_type: Element type of the move (e.g., "Electric")
        :param defender_type: Defender's type (e.g., "Water")
        :return: Effectiveness multiplier as float (e.g., 0.5, 1.0, 2.0)
        """
        return self.type_chart.loc[attack_type, defender_type]

    @staticmethod
    def get_random_damage_multiplier():
        """
        Return a random multiplier between 0.85 and 1.00,
        simulating in-game damage variation using a non-uniform distribution.

        :return: Multiplier as float
        """
        weighted_values = (
                [85, 87, 89, 90, 92, 94, 96, 98] * 3 +  # ~7.69% each
                [86, 88, 91, 93, 95, 97, 99] * 2 +  # ~5.13% each
                [100]  # ~2.56%
        )
        random_multiplier = random.choice(weighted_values)
        print(f"Random damage multiplier (R): {random_multiplier} → factor {random_multiplier / 100:.2f}")
        return random_multiplier / 100

    @staticmethod
    def is_crit_hit(pokemon):
        """
        Determine whether the move is a critical hit based on the attacker's crit chance.

        :param pokemon: The attacking Pokémon
        :return: True if it's a critical hit, False otherwise
        """
        return random.random() <= pokemon.base_stats.get_crit_chance()

    @staticmethod
    def move_hit(move):
        """
        Determine whether the move successfully hits, based on its accuracy.

        :param move: The move object
        :return: True if the move hits, False if it misses
        """
        return random.uniform(0, 100) < move.accuracy

    @staticmethod
    def display_damage_range(base_damage, effectiveness):
        """
        Calculate and return the minimum and maximum possible damage values.

        :param base_damage: The base damage before randomness
        :param effectiveness: The effectiveness multiplier
        :return: Tuple (min_damage, max_damage)
        """
        return round(base_damage * 0.85 * effectiveness, 2), round(base_damage * effectiveness, 2)

    def calculate_damage(self, attacker, defender, move):
        """
        Perform a full damage calculation from one Pokémon to another using a move.

        :param attacker: The attacking Pokémon
        :param defender: The defending Pokémon
        :param move: The move being used
        :return: An Attack object with detailed result data
        """

        # Step 1: Check if the move hits
        if not self.move_hit(move):
            print(f"{attacker.name}'s {move.name} missed!")
            return Attack(
                damage_range=(0, 0),
                effective_damage=0.0,
                missed=True,
                crit=False,
                effectiveness=0.0,
                defender=copy.deepcopy(defender),
                attacker=copy.deepcopy(attacker),
                move=copy.deepcopy(move)
            )

        # Step 2: Determine critical hit and which stats to use
        is_crit = self.is_crit_hit(attacker)
        defender_stats = defender.base_stats if is_crit else defender.current_stats

        # Step 3: Choose relevant attack/defense stats depending on move category
        if move.damage_class == 'physical':
            attack_stat = attacker.current_stats.attack
            defense_stat = defender_stats.defense
        else:
            attack_stat = attacker.current_stats.attack_spe
            defense_stat = defender_stats.defense_spe

        # Step 4: Apply base damage formula
        base_damage = (((2 * attacker.level / 5 + 2) * move.damage * (attack_stat / defense_stat)) / 50) + 2

        # Step 5: Apply STAB (Same-Type Attack Bonus)
        if move.element == attacker.type1 or move.element == attacker.type2:
            base_damage *= 1.5

        # Step 6: Apply type effectiveness multiplier
        effectiveness = self.get_effectiveness(move.element, defender.type1)
        if defender.type2:
            effectiveness *= self.get_effectiveness(move.element, defender.type2)

        # Step 7: Display damage range (for info/logging)
        damage_range = self.display_damage_range(base_damage, effectiveness)
        print(f"Damage Range {damage_range[0]} - {damage_range[1]}")

        # Step 8: Apply critical damage bonus if needed
        if is_crit:
            base_damage *= 1.5

        # Step 9: Apply random factor to simulate real in-game variance
        random_factor = self.get_random_damage_multiplier()

        # Step 10: Return full attack result as a dataclass
        return Attack(
            damage_range=damage_range,
            effective_damage=base_damage * effectiveness * random_factor,
            missed=False,
            crit=is_crit,
            effectiveness=effectiveness,
            defender=copy.deepcopy(defender),
            attacker=copy.deepcopy(attacker),
            move=copy.deepcopy(move)
        )
