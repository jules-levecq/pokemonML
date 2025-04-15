import math

# Tables used to calculate critical hit chance and accuracy/evasion modifiers
tabCritChance = [0.0625, 0.125, 0.5, 1.0]
tabAccuracyEvasion = [0.33, 0.38, 0.43, 0.5, 0.6, 0.75, 1, 1.33, 1.67, 2, 2.33, 2.67, 3]


class IndividualValues:
    """Represents Pokémon's Individual Values (IVs), which influence each stat's potential."""
    def __init__(self, health=31, attack=31, defense=31, attack_spe=31, defense_spe=31, speed=31):
        self.health = health
        self.attack = attack
        self.defense = defense
        self.attack_spe = attack_spe
        self.defense_spe = defense_spe
        self.speed = speed

    def __repr__(self):
        return (
            f"IndividualValues(HP={self.health}, ATK={self.attack}, DEF={self.defense}, "
            f"SATK={self.attack_spe}, SDEF={self.defense_spe}, SPD={self.speed})"
        )


class EffortValues:
    """Represents Pokémon's Effort Values (EVs), which accumulate and influence stats over time."""
    def __init__(self, health=0, attack=0, defense=0, attack_spe=0, defense_spe=0, speed=0):
        self.health = health
        self.attack = attack
        self.defense = defense
        self.attack_spe = attack_spe
        self.defense_spe = defense_spe
        self.speed = speed

    def __repr__(self):
        return (
            f"EffortValues(HP={self.health}, ATK={self.attack}, DEF={self.defense}, "
            f"SATK={self.attack_spe}, SDEF={self.defense_spe}, SPD={self.speed})"
        )


class Stats:
    """
    Represents a Pokémon's full set of battle stats, including base values,
    IVs, EVs, and in-battle modifiers like accuracy, evasion and crit chance.
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
        self.accuracy = 6  # Neutral value (1.0 multiplier)
        self.evasion = 6   # Neutral value (1.0 multiplier)
        self.critChance = 0  # Default crit stage

    # --- Factory / Clone ---

    def clone(self):
        """Return a full copy of the Stats object."""
        return Stats(
            self.health, self.attack, self.defense, self.attack_spe,
            self.defense_spe, self.speed, iv=self.iv, ev=self.ev
        )

    @classmethod
    def from_csv_row(cls, row, level):
        """Create a Stats object from a CSV row by calculating real stats for a given level."""
        base_stats = cls(
            health=int(row["HP"]),
            attack=int(row["Attack"]),
            defense=int(row["Defense"]),
            attack_spe=int(row["Sp. Atk"]),
            defense_spe=int(row["Sp. Def"]),
            speed=int(row["Speed"])
        )
        return cls(
            health=base_stats.calculate_hp(level),
            attack=base_stats.calculate_stat("Attack", level),
            defense=base_stats.calculate_stat("Defense", level),
            attack_spe=base_stats.calculate_stat("Sp. Atk", level),
            defense_spe=base_stats.calculate_stat("Sp. Def", level),
            speed=base_stats.calculate_stat("Speed", level)
        )

    # --- Calculations ---

    def calculate_hp(self, level: int) -> int:
        """Compute HP based on level, base stat, IV and EV."""
        iv = self.iv.health
        base = self.health
        ev = self.ev.health
        return math.floor(((iv + 2 * base + (ev // 4)) * level) / 100) + level + 10

    def calculate_stat(self, stat_name: str, level: int, nature: float = 1.0) -> int:
        """Compute a regular stat (Attack, Defense...) with optional nature modifier."""
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
        raw_stat = math.floor(((iv + 2 * base + (ev // 4)) * level) / 100) + 5
        return math.floor(raw_stat * nature)

    # --- Crit Management ---

    def increase_crit_chance(self):
        """Raise the crit stage by 1, up to 3."""
        if self.critChance < 3:
            self.critChance += 1
        else:
            print("Critical hit chance is already at its maximum!")

    def decrease_crit_chance(self):
        """Lower the crit stage by 1, down to 0."""
        if self.critChance > 0:
            self.critChance -= 1
        else:
            print("Critical hit chance cannot go lower!")

    def get_crit_chance(self):
        """Return the current critical hit probability."""
        return tabCritChance[self.critChance]

    # --- Accuracy Management ---

    def increase_accuracy(self):
        """Raise accuracy stage (max 12)."""
        if self.accuracy < 12:
            self.accuracy += 1
        else:
            print("Accuracy is already at its maximum!")

    def decrease_accuracy(self):
        """Lower accuracy stage (min 0)."""
        if self.accuracy > 0:
            self.accuracy -= 1
        else:
            print("Accuracy cannot go lower!")

    def get_accuracy(self):
        """Get the current accuracy multiplier."""
        return tabAccuracyEvasion[self.accuracy]

    # --- Evasion Management ---

    def increase_evasion(self):
        """Raise evasion stage (max 12)."""
        if self.evasion < 12:
            self.evasion += 1
        else:
            print("Evasion is already at its maximum!")

    def decrease_evasion(self):
        """Lower evasion stage (min 0)."""
        if self.evasion > 0:
            self.evasion -= 1
        else:
            print("Evasion cannot go lower!")

    def get_evasion(self):
        """Get the current evasion multiplier."""
        return tabAccuracyEvasion[self.evasion]

    # --- Debug ---

    def __repr__(self):
        return (f"Stats(HP={self.health}, ATK={self.attack}, DEF={self.defense}, "
                f"SATK={self.attack_spe}, SDEF={self.defense_spe}, SPD={self.speed})")
