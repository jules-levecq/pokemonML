class Move:
    """Class representing a Pokémon move."""
    def __init__(self, name, element, damage, category, accuracy, pp):
        """
        Initialize a move.
        :param name: Name of the move
        :param element: Type of the move (e.g., Electric, Grass)
        :param damage: Base damage to the move
        :param category: Damage category ('physical' or 'special')
        :param accuracy: Accuracy percentage of the move
        """
        self.name = name
        self.element = element
        self.damage = damage
        self.damage_class = category  # "physical" or "special"
        self.accuracy = accuracy
        self.pp = pp

    # --- Factory ---

    @classmethod
    def from_csv_row(cls, row):
        """
        Create a Move object from a CSV row (as a pandas Series).
        :param row: Pandas Series with move data
        :return: Move instance
        """
        return cls(
            name=row['name'],
            element=row['type'],
            damage=int(row['power']),
            category=row['damage_class'].lower(),
            accuracy=int(row['accuracy']),
            pp=int(row['pp'])
        )
