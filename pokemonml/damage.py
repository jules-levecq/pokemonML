import random
import copy
from dataclasses import dataclass
from .utils import read_csv_data
from .create_pokemon import Pokemon
from .moves import Move


@dataclass
class Attack:
    """
    Data class representing the result of a single damage calculation.

    This object stores the full context of an attack, including whether the move hit,
    how much damage it dealt, whether it was a critical hit, and how effective it was.

    Attributes:
        damage_range (tuple): Theoretical min and max damage of the move.
        effective_damage (float): The actual damage that was inflicted.
        missed (bool): True if the move missed, False otherwise.
        crit (bool): True if it was a critical hit.
        effectiveness (float): Type effectiveness multiplier (e.g. 2.0, 0.5).
        defender (Pokemon): A deep copy of the defender at the time of the attack.
        attacker (Pokemon): A deep copy of the attacker at the time of the attack.
        move (object): A deep copy of the move that was used.
    """

    damage_range: tuple
    effective_damage: float
    missed: bool
    crit: bool
    effectiveness: float
    defender: Pokemon
    attacker: Pokemon
    move: Move

    def __repr__(self):
        """
        Return a short human-readable description of the attack.

        Returns:
            str: A string summarizing the move, damage dealt, and hit/crit status.
        """
        return f"{self.move.name} → {self.effective_damage:.2f} dmg, crit: {self.crit}, miss: {self.missed}"  # type: ignore[attr-defined]


class PokemonDamageCalculator:
    """
    Core class for handling Pokémon damage calculations and battle interactions.

    This class encapsulates all the logic related to calculating damage based on
    stats, move accuracy, type effectiveness, critical hits, and PP management.

    It is designed to be modular and extendable for both simulation and ML data generation.

    Attributes:
        type_chart (pd.DataFrame): Type effectiveness matrix indexed by attacking type.
        verbose (bool): If True, print logs and debug information during calculations.
    """

    def __init__(self, csv_path, verbose=False):
        """
        Initialize the calculator and load the type chart from a CSV file.

        Args:
            csv_path (str): Path to the CSV file with type effectiveness chart.
            verbose (bool): Whether to print debug/log info during calculations.
        """
        type_chart_df = read_csv_data(csv_path)
        type_chart_df.set_index('Attacking', inplace=True)
        self.type_chart = type_chart_df
        self.verbose = verbose

    # --- Static Helpers ---

    def get_effectiveness(self, attack_type, defender_type):
        """
        Get the effectiveness multiplier for a move type against a given defender type.

        Args:
            attack_type (str): The attacking move's elemental type.
            defender_type (str): The target Pokémon's elemental type.

        Returns:
            float: The type effectiveness multiplier.
        """
        return self.type_chart.loc[attack_type, defender_type]

    def get_random_damage_multiplier(self, is_random=True):
        """
        Return a damage multiplier in the range [0.85, 1.00] following Pokémon's random spread.

        Args:
            is_random (bool): If False, use the average multiplier (for deterministic simulations).

        Returns:
            float: A multiplier for base damage variation.
        """
        weighted_values = (
            [85, 87, 89, 90, 92, 94, 96, 98] * 3 +
            [86, 88, 91, 93, 95, 97, 99] * 2 +
            [100]
        )
        if is_random:
            r = random.choice(weighted_values)
            if self.verbose:
                print(f"Random damage multiplier (R): {r} → factor {r / 100:.2f}")
            return r / 100
        return sum(weighted_values) / len(weighted_values) / 100

    @staticmethod
    def is_crit_hit(pokemon):
        """
        Determine if the attack will result in a critical hit.

        Args:
            pokemon (Pokemon): The attacking Pokémon.

        Returns:
            bool: True if a critical hit occurs.
        """
        return random.random() <= pokemon.base_stats.get_crit_chance()

    @staticmethod
    def move_hit(move):
        """
        Determine if the move hits based on its accuracy.

        Args:
            move (Move): The move being used.

        Returns:
            bool: True if the move lands, False otherwise.
        """
        return random.uniform(0, 100) < move.accuracy

    @staticmethod
    def display_damage_range(base_damage, effectiveness):
        """
        Return the min and max damage possible after applying effectiveness.

        Args:
            base_damage (float): Raw base damage.
            effectiveness (float): Type effectiveness multiplier.

        Returns:
            tuple: (min_damage, max_damage)
        """
        return round(base_damage * 0.85 * effectiveness, 2), round(base_damage * effectiveness, 2)

    @staticmethod
    def _clone_battle_state(attacker, defender, move):
        """
        Clone all objects involved in the attack (for logging or analysis purposes).

        Returns:
            tuple: (attacker_copy, defender_copy, move_copy)
        """
        return copy.deepcopy(attacker), copy.deepcopy(defender), copy.deepcopy(move)

    def _build_attack(self, effective_damage, crit, effectiveness, damage_range, missed, attacker, defender, move):
        """
        Build a full Attack object with deep copies of all participants.

        Returns:
            Attack: Complete attack result object.
        """
        atk_, def_, move_ = self._clone_battle_state(attacker, defender, move)
        return Attack(
            damage_range=damage_range,
            effective_damage=effective_damage,
            missed=missed,
            crit=crit,
            effectiveness=effectiveness,
            defender=def_,
            attacker=atk_,
            move=move_
        )

    def _return_miss_attack(self, attacker, defender, move, reason="missed"):
        """
        Generate an Attack result when the move fails to land.

        Args:
            attacker (Pokemon): The attacker.
            defender (Pokemon): The target.
            move (Move): The move used.
            reason (str): Description for why the attack missed.

        Returns:
            Attack: An empty attack (0 damage).
        """
        if self.verbose:
            print(f"{attacker.name}'s {move.name} {reason}!")
        return self._build_attack(0.0, False, 0.0, (0, 0), True, attacker, defender, move)

    # --- Core Damage Logic ---

    def compute_base_damage(self, attacker, defender, move, is_crit=False, random_multiplier=True):
        """
        Compute the raw base damage value before rounding or applying game effects.

        Args:
            attacker (Pokemon): The attacker.
            defender (Pokemon): The defender.
            move (Move): The move used.
            is_crit (bool): Whether to bypass stat drops.
            random_multiplier (bool): Whether to include randomness.

        Returns:
            tuple: (base_damage, effectiveness, random_factor, damage_range)
        """
        if move.damage_class == 'physical':
            attack_stat = attacker.base_stats.attack if is_crit else attacker.current_stats.attack
            defense_stat = defender.base_stats.defense if is_crit else defender.current_stats.defense
        else:
            attack_stat = attacker.base_stats.attack_spe if is_crit else attacker.current_stats.attack_spe
            defense_stat = defender.base_stats.defense_spe if is_crit else defender.current_stats.defense_spe

        base_damage = (((2 * attacker.level / 5 + 2) * move.damage * (attack_stat / defense_stat)) / 50) + 2

        if move.element in [attacker.type1, attacker.type2]:
            base_damage *= 1.5

        effectiveness = self.get_effectiveness(move.element, defender.type1)
        if defender.type2:
            effectiveness *= self.get_effectiveness(move.element, defender.type2)

        damage_range = self.display_damage_range(base_damage, effectiveness)
        if self.verbose:
            print(f"Damage Range {damage_range[0]} - {damage_range[1]}")

        random_factor = self.get_random_damage_multiplier(random_multiplier)
        return base_damage, effectiveness, random_factor, damage_range

    def compute_theoretical_attack(self, attacker, defender, move, is_crit, random_multiplier):
        """
        Run a theoretical attack calculation without applying any real effects.
        
        Modified Behavior:
        - If the lower bound of the damage range (damage_range[0]) is greater than or equal 
        to the defender's current HP, then we set effective_damage to the defender's current HP,
        as no more damage can be inflicted (KO is certain).
        - Otherwise, effective_damage is set to -1, indicating that the effective damage is not fixed 
        and should only be computed during the actual interaction.
        
        Args:
            attacker (Pokemon): The attacking Pokémon.
            defender (Pokemon): The defending Pokémon.
            move (Move): The move to evaluate.
            is_crit (bool): Force a critical hit evaluation.
            random_multiplier (bool): Enable or disable the random damage factor.
        
        Returns:
            Attack: A simulated attack result object containing the computed damage range,
                    a critical hit flag, and an effective_damage field set as described.
        """
        base_damage, effectiveness, random_factor, damage_range = self.compute_base_damage(attacker, defender, move, is_crit, random_multiplier)
        
        # Check if the minimum possible damage is sufficient to KO the defender.
        if damage_range[0] >= defender.current_stats.health:
            effective_damage = defender.current_stats.health
        else:
            effective_damage = -1
        
        return self._build_attack(effective_damage, is_crit, effectiveness, damage_range, False, attacker, defender, move)

    def calculate_damage(self, attacker, defender, move, random_multiplier=True):
        """
        Perform a full damage calculation, considering all possible failure points.

        Args:
            attacker (Pokemon): The attacking Pokémon.
            defender (Pokemon): The defending Pokémon.
            move (Move): The move being executed.
            random_multiplier (bool): Use randomized damage values.

        Returns:
            Attack: Fully resolved damage instance.
        """
        if move.pp <= 0:
            return self._return_miss_attack(attacker, defender, move, reason="has no PP left")
        if not self.move_hit(move):
            return self._return_miss_attack(attacker, defender, move)

        is_crit = self.is_crit_hit(attacker)
        base_damage, effectiveness, random_factor, damage_range = self.compute_base_damage(attacker, defender, move, is_crit, random_multiplier)

        if is_crit:
            base_damage *= 1.5

        return self._build_attack(int(base_damage * effectiveness * random_factor), is_crit, effectiveness, damage_range, False, attacker, defender, move)

    def resolve_interaction(self, attacker, defender, move, random_multiplier=True) -> Attack:
        """
        Run a full attack and apply real effects: damage taken and PP used.

        Args:
            attacker (Pokemon): Attacking Pokémon.
            defender (Pokemon): Defending Pokémon.
            move (Move): Move being executed.
            random_multiplier (bool): Whether to apply randomized damage.

        Returns:
            Attack: Final result of the turn.
        """
        damage_result = self.calculate_damage(attacker, defender, move, random_multiplier=random_multiplier)

        if not damage_result.missed:
            defender.take_damage(damage_result.effective_damage)
            if self.verbose:
                print(f"{attacker.name} dealt {damage_result.effective_damage:.2f} to {defender.name}")

        for m in attacker.moves:
            if m.name == move.name:
                m.pp = max(0, m.pp - 1)
                used_move = m
                break
        else:
            used_move = move
            if self.verbose:
                print(f"Warning: {move.name} not found in {attacker.name}'s move list!")

        return self._build_attack(
            damage_result.effective_damage,
            damage_result.crit,
            damage_result.effectiveness,
            damage_result.damage_range,
            damage_result.missed,
            attacker,
            defender,
            used_move
        )
