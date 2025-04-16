import math

# Critical hit chance by stage level (index 0 = base, 3 = max boost)
tabCritChance = [0.0625, 0.125, 0.5, 1.0]

# Accuracy and evasion stage multipliers (index 6 = neutral = 1.0)
tabAccuracyEvasion = [0.33, 0.38, 0.43, 0.5, 0.6, 0.75, 1, 1.33, 1.67, 2, 2.33, 2.67, 3]


class IndividualValues:
    """
    Represents Pokémon's Individual Values (IVs), which define the innate potential of each stat.

    IVs are permanent and fixed at birth. They affect the final calculated stats.

    Attributes:
        health (int): IV for HP (default: 31)
        attack (int): IV for physical attack (default: 31)
        defense (int): IV for physical defense (default: 31)
        attack_spe (int): IV for special attack (default: 31)
        defense_spe (int): IV for special defense (default: 31)
        speed (int): IV for speed (default: 31)
    """

    def __init__(self, health=31, attack=31, defense=31, attack_spe=31, defense_spe=31, speed=31):
        self.health = health
        self.attack = attack
        self.defense = defense
        self.attack_spe = attack_spe
        self.defense_spe = defense_spe
        self.speed = speed

    def __repr__(self):
        return (f"IndividualValues(HP={self.health}, ATK={self.attack}, DEF={self.defense}, "
                f"SATK={self.attack_spe}, SDEF={self.defense_spe}, SPD={self.speed})")


class EffortValues:
    """
    Represents a Pokémon's Effort Values (EVs), earned through battles or training.

    EVs accumulate gradually and affect the final calculated stats.

    Attributes:
        health (int): EV for HP (default: 0)
        attack (int): EV for physical attack (default: 0)
        defense (int): EV for physical defense (default: 0)
        attack_spe (int): EV for special attack (default: 0)
        defense_spe (int): EV for special defense (default: 0)
        speed (int): EV for speed (default: 0)
    """

    def __init__(self, health=0, attack=0, defense=0, attack_spe=0, defense_spe=0, speed=0):
        self.health = health
        self.attack = attack
        self.defense = defense
        self.attack_spe = attack_spe
        self.defense_spe = defense_spe
        self.speed = speed

    def __repr__(self):
        return (f"EffortValues(HP={self.health}, ATK={self.attack}, DEF={self.defense}, "
                f"SATK={self.attack_spe}, SDEF={self.defense_spe}, SPD={self.speed})")


class Stats:
    """
    Represents a Pokémon's complete set of combat stats, including modifiers and real-time state.

    This object merges base stats, IVs, EVs, level, and battle modifiers such as accuracy,
    evasion, and crit stage.

    Attributes:
        health (int): Base HP stat.
        attack (int): Base physical attack stat.
        defense (int): Base physical defense stat.
        attack_spe (int): Base special attack stat.
        defense_spe (int): Base special defense stat.
        speed (int): Base speed stat.
        iv (IndividualValues): Individual values object.
        ev (EffortValues): Effort values object.
        accuracy (int): Stage of accuracy modifier (0–12, default: 6).
        evasion (int): Stage of evasion modifier (0–12, default: 6).
        critChance (int): Stage of crit chance (0–3).
    """

    def __init__(self, health, attack, defense, attack_spe, defense_spe, speed, iv=None, ev=None):
        self.health = health
        self.attack = attack
        self.defense = defense
        self.attack_spe = attack_spe
        self.defense_spe = defense_spe
        self.speed = speed
        self.iv = iv if iv is not None else IndividualValues()
        self.ev = ev if ev is not None else EffortValues()
        self.accuracy = 6
        self.evasion = 6
        self.critChance = 0

    # --- Factory / Clone ---

    def clone(self):
        """
        Create a deep copy of the stats object.

        Returns:
            Stats: New Stats instance with same values.
        """
        return Stats(
            self.health, self.attack, self.defense,
            self.attack_spe, self.defense_spe, self.speed,
            iv=self.iv, ev=self.ev
        )

    @classmethod
    def from_csv_row(cls, row, level):
        """
        Generate a Stats object from CSV data and compute actual stats based on level.

        Args:
            row (pd.Series): Row of the Pokémon CSV containing base stats.
            level (int): Level of the Pokémon.

        Returns:
            Stats: Final calculated stats including IVs, EVs, and level adjustments.
        """
        base = cls(
            health=int(row["HP"]),
            attack=int(row["Attack"]),
            defense=int(row["Defense"]),
            attack_spe=int(row["Sp. Atk"]),
            defense_spe=int(row["Sp. Def"]),
            speed=int(row["Speed"])
        )
        return cls(
            health=base.calculate_hp(level),
            attack=base.calculate_stat("Attack", level),
            defense=base.calculate_stat("Defense", level),
            attack_spe=base.calculate_stat("Sp. Atk", level),
            defense_spe=base.calculate_stat("Sp. Def", level),
            speed=base.calculate_stat("Speed", level)
        )

    # --- Stat Calculations ---

    def calculate_hp(self, level: int) -> int:
        """
        Calculate final HP stat based on formula.

        Returns:
            int: The final HP stat.
        """
        iv = self.iv.health
        base = self.health
        ev = self.ev.health
        return math.floor(((iv + 2 * base + (ev // 4)) * level) / 100) + level + 10

    def calculate_stat(self, stat_name: str, level: int, nature: float = 1.0) -> int:
        """
        Calculate a stat value at a given level, optionally adjusted by nature.

        Args:
            stat_name (str): One of 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed'.
            level (int): Pokémon's level.
            nature (float): Nature modifier (default: 1.0 = neutral).

        Returns:
            int: Final computed stat value.
        """
        if stat_name == "Attack":
            base, iv, ev = self.attack, self.iv.attack, self.ev.attack
        elif stat_name == "Defense":
            base, iv, ev = self.defense, self.iv.defense, self.ev.defense
        elif stat_name == "Sp. Atk":
            base, iv, ev = self.attack_spe, self.iv.attack_spe, self.ev.attack_spe
        elif stat_name == "Sp. Def":
            base, iv, ev = self.defense_spe, self.iv.defense_spe, self.ev.defense_spe
        elif stat_name == "Speed":
            base, iv, ev = self.speed, self.iv.speed, self.ev.speed
        else:
            raise ValueError(f"Invalid stat_name: {stat_name}")

        raw = math.floor(((iv + 2 * base + (ev // 4)) * level) / 100) + 5
        return math.floor(raw * nature)

    # --- Critical Hit Logic ---

    def increase_crit_chance(self):
        """Increment crit stage up to max (3)."""
        if self.critChance < 3:
            self.critChance += 1
        else:
            print("Critical hit chance is already at its maximum!")

    def decrease_crit_chance(self):
        """Decrement crit stage down to min (0)."""
        if self.critChance > 0:
            self.critChance -= 1
        else:
            print("Critical hit chance cannot go lower!")

    def get_crit_chance(self):
        """Get the actual probability of landing a critical hit."""
        return tabCritChance[self.critChance]

    # --- Accuracy & Evasion ---

    def increase_accuracy(self):
        """Increase accuracy stage by 1 (max 12)."""
        if self.accuracy < 12:
            self.accuracy += 1
        else:
            print("Accuracy is already at its maximum!")

    def decrease_accuracy(self):
        """Decrease accuracy stage by 1 (min 0)."""
        if self.accuracy > 0:
            self.accuracy -= 1
        else:
            print("Accuracy cannot go lower!")

    def get_accuracy(self):
        """Get the current accuracy multiplier (float)."""
        return tabAccuracyEvasion[self.accuracy]

    def increase_evasion(self):
        """Increase evasion stage by 1 (max 12)."""
        if self.evasion < 12:
            self.evasion += 1
        else:
            print("Evasion is already at its maximum!")

    def decrease_evasion(self):
        """Decrease evasion stage by 1 (min 0)."""
        if self.evasion > 0:
            self.evasion -= 1
        else:
            print("Evasion cannot go lower!")

    def get_evasion(self):
        """Get the current evasion multiplier (float)."""
        return tabAccuracyEvasion[self.evasion]

    # --- Debugging ---

    def __repr__(self):
        """Human-readable summary of all base stat values."""
        return (f"Stats(HP={self.health}, ATK={self.attack}, DEF={self.defense}, "
                f"SATK={self.attack_spe}, SDEF={self.defense_spe}, SPD={self.speed})")
