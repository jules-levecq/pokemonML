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