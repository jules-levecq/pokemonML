import math

# Tables used to calculate critical hit chance and accuracy/evasion modifiers
tabCritChance = [0.0625, 0.125, 0.5, 1.0]
tabAccuracyEvasion = [0.33, 0.38, 0.43, 0.5, 0.6, 0.75, 1, 1.33, 1.67, 2, 2.33, 2.67, 3]


class IndividualValues:
    """
    Class representing a Pokémon's Individual Values (IVs).

    IVs are innate values that determine a Pokémon's potential in each stat.
    By default, each stat is set to 31, the maximum possible value according to standard game mechanics.

    Attributes:
        health (int): IV for HP. Default is 31.
        attack (int): IV for physical attack. Default is 31.
        defense (int): IV for physical defense. Default is 31.
        special_attack (int): IV for special attack. Default is 31.
        special_defense (int): IV for special defense. Default is 31.
        speed (int): IV for speed. Default is 31.
    """
    def __init__(self, health=31, attack=31, defense=31, special_attack=31, special_defense=31, speed=31):
        self.health = health
        self.attack = attack
        self.defense = defense
        self.special_attack = special_attack
        self.special_defense = special_defense
        self.speed = speed

    def __repr__(self):
        return (
            f"IndividualValues(HP={self.health}, ATK={self.attack}, DEF={self.defense}, "
            f"SATK={self.special_attack}, SDEF={self.special_defense}, SPD={self.speed})"
        )


class EffortValues:
    """
    Class representing a Pokémon's Effort Values (EVs).

    EVs are points gained through battle that contribute to a Pokémon's stat growth.
    They are usually accumulated over time and are set to 0 by default.

    Attributes:
        health (int): EV for HP. Default is 0.
        attack (int): EV for physical attack. Default is 0.
        defense (int): EV for physical defense. Default is 0.
        special_attack (int): EV for special attack. Default is 0.
        special_defense (int): EV for special defense. Default is 0.
        speed (int): EV for speed. Default is 0.
    """
    def __init__(self, health=0, attack=0, defense=0, special_attack=0, special_defense=0, speed=0):
        self.health = health
        self.attack = attack
        self.defense = defense
        self.special_attack = special_attack
        self.special_defense = special_defense
        self.speed = speed

    def __repr__(self):
        return (
            f"EffortValues(HP={self.health}, ATK={self.attack}, DEF={self.defense}, "
            f"SATK={self.special_attack}, SDEF={self.special_defense}, SPD={self.speed})"
        )


class Stats:
    """
    Class representing a Pokémon's battle statistics.

    This class consolidates the base stats of a Pokémon along with its Individual Values (IVs)
    and Effort Values (EVs). These components combine to determine the final stats used in battle
    calculations. In addition, the class includes modifiers for accuracy, evasion, and critical hit chance,
    which can be used to simulate in-game stat adjustments.

    Attributes:
        health (int): Base HP value.
        attack (int): Base physical attack value.
        defense (int): Base physical defense value.
        attack_spe (int): Base special attack value.
        defense_spe (int): Base special defense value.
        speed (int): Base speed value.
        iv (IndividualValues): Instance containing individual value details.
        ev (EffortValues): Instance containing effort value details.
        accuracy (int): Modifier index for accuracy; default is 6 (neutral, equals a 1.0 multiplier).
        evasion (int): Modifier index for evasion; default is 6 (neutral, equals a 1.0 multiplier).
        critChance (int): Modifier level for critical hit chance; default is 0.
    """

    def __init__(self, health, attack, defense, attack_spe, defense_spe, speed, iv=None, ev=None):
        self.health = health
        self.attack = attack
        self.defense = defense
        self.attack_spe = attack_spe
        self.defense_spe = defense_spe
        self.speed = speed

        # Initialize IVs and EVs using provided values or defaults
        self.iv = iv if iv is not None else IndividualValues()
        self.ev = ev if ev is not None else EffortValues()

        # Modifiers: 0–3 for crit chance, 0–12 for accuracy/evasion
        self.accuracy = 6      # Neutral index (index 6 corresponds to x1.0)
        self.evasion = 6       # Neutral index
        self.critChance = 0    # Base critical hit chance

    # ------------------------
    # Calculate Stats management
    # ------------------------

    def calculate_hp(self, level: int) -> int:
        """
        Calculate the final HP stat based on the formula:

            HP = floor(((IV + 2 * Base + (EV / 4)) * Level) / 100) + Level + 10

        Args:
            level (int): The current level of the Pokémon.

        Returns:
            int: The final HP value, after rounding down.
        """
        # IV, Base, and EV for HP
        iv = self.iv.health
        base = self.health
        ev = self.ev.health

        return math.floor(((iv + 2 * base + (ev // 4)) * level) / 100) + level + 10

    def calculate_stat(self, stat_name: str, level: int, nature: float = 1.0) -> int:
        """
        Calculate the final value of a given stat (Attack, Defense, Sp. Atk, Sp. Def, Speed)
        using the standard Pokémon formula:

            Stat = floor( ( floor(((IV + 2 * Base + (EV / 4)) * Level) / 100) + 5 ) * Nature )

        Args:
            stat_name (str): The name of the stat to calculate (one of "attack", "defense",
                             "special_attack", "special_defense", "speed").
            level (int): The current level of the Pokémon.
            nature (float): Nature multiplier (e.g., 1.1 for beneficial nature, 0.9 for hindering).

        Returns:
            int: The final stat value, after rounding down.
        """
        # Retrieve the base stat, IV, and EV for the requested stat_name
        if stat_name == "attack":
            base = self.attack
            iv = self.iv.attack
            ev = self.ev.attack
        elif stat_name == "defense":
            base = self.defense
            iv = self.iv.defense
            ev = self.ev.defense
        elif stat_name == "special_attack":
            base = self.attack_spe
            iv = self.iv.special_attack
            ev = self.ev.special_attack
        elif stat_name == "special_defense":
            base = self.defense_spe
            iv = self.iv.special_defense
            ev = self.ev.special_defense
        elif stat_name == "speed":
            base = self.speed
            iv = self.iv.speed
            ev = self.ev.speed
        else:
            raise ValueError(f"Invalid stat_name: {stat_name}")

        # Compute the raw stat part (floor(...) + 5)
        raw_stat = math.floor(((iv + 2 * base + (ev // 4)) * level) / 100) + 5

        # Apply the nature multiplier, then floor again
        final_stat = math.floor(raw_stat * nature)
        return final_stat

    # ------------------------
    # Critical hit management
    # ------------------------

    def increase_crit_chance(self):
        """Increase the critical hit chance level by 1 (max is 3)."""
        if self.critChance < 3:
            return self.critChance + 1
        print("Critical hit chance is already at its maximum!")

    def decrease_crit_chance(self):
        """Decrease the critical hit chance level by 1 (min is 0)."""
        if self.critChance > 0:
            return self.critChance - 1
        print("Critical hit chance cannot go lower!")

    def get_crit_chance(self):
        """
        Get the actual critical hit chance value based on the critChance index.
        :return: Float between 0.0625 and 1.0
        """
        return tabCritChance[self.critChance]

    # ------------------------
    # Accuracy management
    # ------------------------

    def increase_accuracy(self):
        """Increase the accuracy level (max index is 12)."""
        if self.accuracy < 12:
            return self.accuracy + 1
        print("Accuracy is already at its maximum!")

    def decrease_accuracy(self):
        """Decrease the accuracy level (min index is 0)."""
        if self.accuracy > 0:
            return self.accuracy - 1
        print("Accuracy cannot go lower!")

    def get_accuracy(self):
        """
        Get the current accuracy multiplier based on the accuracy index.
        :return: Float between 0.33 and 3.0
        """
        return tabAccuracyEvasion[self.accuracy]

    # ------------------------
    # Evasion management
    # ------------------------

    def increase_evasion(self):
        """Increase the evasion level (max index is 12)."""
        if self.evasion < 12:
            return self.evasion + 1
        print("Evasion is already at its maximum!")

    def decrease_evasion(self):
        """Decrease the evasion level (min index is 0)."""
        if self.evasion > 0:
            return self.evasion - 1
        print("Evasion cannot go lower!")

    def get_evasion(self):
        """
        Get the current evasion multiplier based on the evasion index.
        :return: Float between 0.33 and 3.0
        """
        return tabAccuracyEvasion[self.evasion]

    # ------------------------
    # Clone Stats
    # ------------------------

    def clone(self):
        """Return a copy of the Stats object."""
        return Stats(
            self.health, self.attack, self.defense,
            self.attack_spe, self.defense_spe, self.speed
        )
