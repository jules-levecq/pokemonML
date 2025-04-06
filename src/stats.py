# Tables used to calculate critical hit chance and accuracy/evasion modifiers
tabCritChance = [0.0625, 0.125, 0.5, 1.0]
tabAccuracyEvasion = [0.33, 0.38, 0.43, 0.5, 0.6, 0.75, 1, 1.33, 1.67, 2, 2.33, 2.67, 3]


class Stats:
    """Class representing a Pokémon's combat statistics, including modifiers."""

    def __init__(self, health, attack, defense, attack_spe, defense_spe, speed):
        """
        Initialize the stats of a Pokémon.
        :param health: HP value
        :param attack: Physical attack value
        :param defense: Physical defense value
        :param attack_spe: Special attack value
        :param defense_spe: Special defense value
        :param speed: Speed value
        """
        self.health = health
        self.attack = attack
        self.defense = defense
        self.attack_spe = attack_spe
        self.defense_spe = defense_spe
        self.speed = speed

        # Modifiers: 0–3 for crit chance, 0–12 for accuracy/evasion
        self.accuracy = 6      # Neutral state (index 6 corresponds to x1.0)
        self.evasion = 6       # Neutral state
        self.critChance = 0    # Base critical hit chance

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

    def clone(self):
        """Return a copy of the Stats object."""
        return Stats(
            self.health, self.attack, self.defense,
            self.attack_spe, self.defense_spe, self.speed
        )
