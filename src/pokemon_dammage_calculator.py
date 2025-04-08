import random
import copy
from dataclasses import dataclass
from .utils import read_csv_data
from .create_pokemon import Pokemon


@dataclass
class Attack:
    """
    Dataclass representing the result of a single attack calculation.
    
    Attributes:
        damage_range (tuple): The minimum and maximum expected damage.
        effective_damage (float): The actual damage dealt after all multipliers.
        missed (bool): Indicates if the move missed.
        crit (bool): Indicates if the attack was a critical hit.
        effectiveness (float): The type effectiveness multiplier.
        defender (Pokémon): A deep copy of the defender's state at the time of attack.
        attacker (Pokémon): A deep copy of the attacker's state at the time of attack.
        move (object): A deep copy of the move used in the attack.
    """
    damage_range: tuple
    effective_damage: float
    missed: bool
    crit: bool
    effectiveness: float
    defender: Pokemon
    attacker: Pokemon
    move: object


class PokemonDamageCalculator:
    """
    Class responsible for computing Pokémon battle damage, integrating various in-game mechanics.

    The computation process is divided into several steps:

    1. **Base Damage Calculation**:
       - Uses the attacking and defending Pokémon's stats, the move's power, and the attacker's level.
       - Applies the Same-Type Attack Bonus (STAB) when applicable.
       - Considers type effectiveness by comparing the move's element with the defender's types.
       - Returns a tuple with (base_damage, effectiveness, random_factor, damage_range), where:
            - base_damage: The computed damage before multipliers.
            - effectiveness: The multiplier due to type interactions.
            - random_factor: A random multiplier (between 0.85 and 1.00) to simulate game variability.
            - damage_range: A tuple showing the theoretical minimum and maximum damage after applying effectiveness.

    2. **Final Base Damage Snapshot**:
       - The method `get_final_base_damage` calls the base damage computation once and uses its result
         to build an `Attack` object with all theoretical details. This method is useful when
         capturing the theoretical output of a move (e.g. for training a deep learning model)
         without applying combat effects such as misses.

    3. **Full Damage Calculation**:
       - The method `calculate_damage` simulates the complete attack: checks if the move hits,
         determines whether a critical hit occurs (which may override the usual stat modifiers),
         and applies randomness. The result is returned as a structured `Attack` object.

    4. **Interaction and State Mutation**:
       - Finally, `return_interaction` applies the actual effects of the attack:
         reducing the defender's HP (if the attack hits) and decrementing the move's PP.
         It returns a post-interaction state snapshot encapsulated in an `Attack` object.

    This modular approach allows you to capture comprehensive attack data,
    which is highly valuable in the context of data analysis and deep learning.
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

        :param is_random: If False, return the average expected multiplier.
        :return: Float between 0.85 and 1.00.
        """
        weighted_values = (
            [85, 87, 89, 90, 92, 94, 96, 98] * 3 +  # ~7.69% each.
            [86, 88, 91, 93, 95, 97, 99] * 2 +       # ~5.13% each.
            [100]                                   # ~2.56%.
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

        :param pokemon: The attacking Pokémon.
        :return: True if it is a critical hit, False otherwise.
        """
        return random.random() <= pokemon.base_stats.get_crit_chance()

    @staticmethod
    def move_hit(move):
        """
        Determine if the move hits based on its accuracy.

        :param move: The move used.
        :return: True if the move hits, False if it misses.
        """
        return random.uniform(0, 100) < move.accuracy

    @staticmethod
    def display_damage_range(base_damage, effectiveness):
        """
        Compute the theoretical min and max damage from the base formula and type effectiveness.

        :param base_damage: The calculated base damage.
        :param effectiveness: The effectiveness multiplier.
        :return: Tuple of (min_damage, max_damage).
        """
        return round(base_damage * 0.85 * effectiveness, 2), round(base_damage * effectiveness, 2)

    def calculate_base_damage(self, attacker, defender, move, is_crit=False, random_multiplier=True):
        """
        Compute the theoretical base damage before applying random variation.

        :param attacker: The attacking Pokémon.
        :param defender: The defending Pokémon.
        :param move: The move used.
        :param is_crit: Boolean indicating whether the attack is a critical hit.
        :param random_multiplier: Boolean indicating whether to include random variation.
        :return: Tuple (base_damage, effectiveness, random_factor, damage_range).
        """
        # Select the appropriate stats based on move category and crit
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

        # Type effectiveness calculation
        effectiveness = self.get_effectiveness(move.element, defender.type1)
        if defender.type2:
            effectiveness *= self.get_effectiveness(move.element, defender.type2)

        damage_range = self.display_damage_range(base_damage, effectiveness)
        print(f"Damage Range {damage_range[0]} - {damage_range[1]}")

        random_factor = self.get_random_damage_multiplier(random_multiplier)
        return base_damage, effectiveness, random_factor, damage_range

    def get_final_base_damage(self, attacker, defender, move, is_crit, random_multiplier):
        """
        Compute the final base damage and return an Attack object with detailed state information.

        This method calculates the theoretical damage to an attack without considering interaction effects
        (e.g. a missed attack). It calls calculate_base_damage once to obtain:
            - base_damage: Damage computed from stats and STAB.
            - effectiveness: Multiplier due to type effectiveness.
            - random_factor: Random variation factor.
            - damage_range: The theoretical minimum and maximum damage after applying the effectiveness multiplier.
        
        The effective damage is computed as:
            effective_damage = base_damage * effectiveness * random_factor
        
        The method then returns an Attack object that includes:
            - The theoretical damage range.
            - The effective damage.
            - The provided flags (missed is always False here, and crit is passed as parameter).
            - Deep copies of the attacker, defender, and move to capture their state at the moment of the attack.

        :param attacker: The attacking Pokémon.
        :param defender: The defending Pokémon.
        :param move: The Move object used.
        :param is_crit: Boolean indicating whether the attack is a critical hit.
        :param random_multiplier: Boolean indicating whether to apply random variation.
        :return: An Attack instance containing complete state data of the attack.
        """
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
        Perform a full damage calculation including move accuracy, critical hit, type effectiveness,
        and random damage variation. Returns a complete attack result as an Attack object.
        
        The process is as follows:
            1. Check if the move hits using move_hit; if not, return an Attack with zero damage.
            2. Determine if the attack is a critical hit with is_crit_hit.
            3. Calculate base damage using calculate_base_damage.
            4. Apply the critical hit modifier if needed.
            5. Compute final damage as the product: base_damage * effectiveness * random_factor.
        
        :param attacker: The attacking Pokémon.
        :param defender: The defending Pokémon.
        :param move: The move used for the attack.
        :param random_multiplier: Boolean indicating whether to apply random damage variation.
        :return: An Attack instance with all details of the calculated attack.
        """
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

        is_crit = self.is_crit_hit(attacker)
        base_damage, effectiveness, random_factor, damage_range = self.calculate_base_damage(
            attacker, defender, move, is_crit, random_multiplier
        )

        if is_crit:
            base_damage *= 1.5

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
    
    def return_interaction(self, attacker, defender, move, random_multiplier=True) -> Attack:
        """
        Simulate an attack interaction by calculating damage and updating the state of both Pokémon.
        
        This function performs the following steps:
            1. Call calculate_damage to compute the attack result.
            2. If the attack did not miss, apply the damage to the defender's current health.
            3. Decrement the PP of the move used (ensuring PP doesn't drop below zero).
            4. Return an Attack object capturing the attack details and the new states of the Pokémon.
        
        :param attacker: The attacking Pokémon.
        :param defender: The defending Pokémon.
        :param move: The move used for the attack.
        :param random_multiplier: Boolean indicating whether to apply random damage variation.
        :return: An Attack instance with updated states after the interaction.
        """
        damage_result = self.calculate_damage(attacker, defender, move, random_multiplier=random_multiplier)
        if not damage_result.missed:
            defender.take_damage(damage_result.effective_damage)
        move.pp -= 1
        if move.pp < 0:
            move.pp = 0

        return Attack(
            damage_range=damage_result.damage_range,
            effective_damage=damage_result.effective_damage,
            missed=damage_result.missed,
            crit=damage_result.crit,
            effectiveness=damage_result.effectiveness,
            defender=copy.deepcopy(defender),
            attacker=copy.deepcopy(attacker),
            move=copy.deepcopy(move)
        )
