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
    Class responsible for computing Pokémon battle damage,
    including move accuracy, critical hits, STAB, and type effectiveness.
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
        Get the type effectiveness multiplier between attack and defense types.

        :param attack_type: The move's element type (e.g., "Electric")
        :param defender_type: The Pokémon's defending type (e.g., "Water")
        :return: Effectiveness multiplier (float)
        """
        return self.type_chart.loc[attack_type, defender_type]

    @staticmethod
    def get_random_damage_multiplier(is_random=True):
        """
        Return a random multiplier between 0.85 and 1.00,
        simulating the in-game non-uniform random variation.

        :param is_random: If False, return the average expected multiplier
        :return: Float between 0.85 and 1.00
        """
        weighted_values = (
            [85, 87, 89, 90, 92, 94, 96, 98] * 3 +  # ~7.69% each
            [86, 88, 91, 93, 95, 97, 99] * 2 +      # ~5.13% each
            [100]                                   # ~2.56%
        )

        if is_random:
            r = random.choice(weighted_values)
            print(f"Random damage multiplier (R): {r} → factor {r / 100:.2f}")
            return r / 100
        return (sum(weighted_values) / len(weighted_values)) / 100

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
        Determine if the move hits based on its accuracy.

        :param move: The move used
        :return: True if the move hits, False if it misses
        """
        return random.uniform(0, 100) < move.accuracy

    @staticmethod
    def display_damage_range(base_damage, effectiveness):
        """
        Compute the theoretical min and max damage from base formula and type effectiveness.

        :param base_damage: The calculated base damage
        :param effectiveness: The effectiveness multiplier
        :return: Tuple of (min_damage, max_damage)
        """
        return round(base_damage * 0.85 * effectiveness, 2), round(base_damage * effectiveness, 2)

    def calculate_base_damage(self, attacker, defender, move, is_crit=False, random_multiplier=True):
        """
        Compute theoretical base damage before applying random variation.

        :param attacker: Attacking Pokémon
        :param defender: Defending Pokémon
        :param move: Move used
        :param is_crit: Whether the hit is critical
        :param random_multiplier: Whether to include random factor in the result
        :return: Tuple (base_damage, effectiveness, random_factor, damage_range)
        """
        # Select relevant stats depending on move type and crit
        if move.damage_class == 'physical':
            attack_stat = attacker.current_stats.attack
            defense_stat = defender.current_stats.defense
        else:
            attack_stat = attacker.current_stats.attack_spe
            defense_stat = defender.current_stats.defense_spe
        if is_crit:
            if move.damage_class == 'physical':
                attack_stat = attacker.base_stats.attack
                defense_stat = defender.base_stats.defense
            else:
                attack_stat = attacker.base_stats.attack_spe
                defense_stat = defender.base_stats.defense_spe

        # Standard damage formula
        base_damage = (((2 * attacker.level / 5 + 2) * move.damage * (attack_stat / defense_stat)) / 50) + 2

        # STAB (Same-Type Attack Bonus)
        if move.element == attacker.type1 or move.element == attacker.type2:
            base_damage *= 1.5

        # Type effectiveness
        effectiveness = self.get_effectiveness(move.element, defender.type1)
        if defender.type2:
            effectiveness *= self.get_effectiveness(move.element, defender.type2)

        damage_range = self.display_damage_range(base_damage, effectiveness)
        print(f"Damage Range {damage_range[0]} - {damage_range[1]}")

        random_factor = self.get_random_damage_multiplier(random_multiplier)
        return base_damage, effectiveness, random_factor, damage_range

    def get_final_base_damage(self, attacker, defender, move, is_crit, random_multiplier):
        base_damage, effectiveness, random_factor, damage_range = self.calculate_base_damage(
            attacker, defender, move, is_crit, random_multiplier
        )
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

    def calculate_damage(self, attacker, defender, move, random_multiplier=True):
        """
        Perform a full damage calculation including accuracy, critical hit, effectiveness,
        and random variation. Returns a complete attack result.

        :param attacker: Attacking Pokémon
        :param defender: Defending Pokémon
        :param move: Move used
        :param random_multiplier: Whether to apply random variation
        :return: Attack dataclass with all relevant results
        """
        # Accuracy check
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

        # Determine critical hit
        is_crit = self.is_crit_hit(attacker)

        # Compute base damage stats
        base_damage, effectiveness, random_factor, damage_range = self.calculate_base_damage(
            attacker, defender, move, is_crit
        )

        # Apply critical modifier if needed
        if is_crit:
            base_damage *= 1.5

        # Final damage
        final_damage = base_damage * effectiveness * random_factor

        return Attack(
            damage_range=damage_range,
            effective_damage=final_damage,
            missed=False,
            crit=is_crit,
            effectiveness=effectiveness,
            defender=copy.deepcopy(defender),
            attacker=copy.deepcopy(attacker),
            move=copy.deepcopy(move)
        )
