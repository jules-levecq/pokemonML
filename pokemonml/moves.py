class Move:
    """
    Represents a single Pokémon move, including its stats and usage constraints.

    A move defines the offensive capability of a Pokémon. It includes its type,
    power, accuracy, damage category (physical or special), and the number of uses (PP).

    Attributes:
        name (str): The unique name of the move (e.g., 'Thunderbolt').
        element (str): The elemental type (e.g., 'Electric', 'Water').
        damage (int): The raw power or base damage the move inflicts.
        damage_class (str): The category of the move: either 'physical' or 'special'.
        accuracy (int): Percentage chance (0-100) that the move will successfully hit.
        pp (int): Power Points indicating how many times the move can be used in total.
    """

    def __init__(self, name, element, damage, category, accuracy, pp, priority=0):
        """
        Initialize a Move object with all required attributes.

        Args:
            name (str): The name of the move.
            element (str): Type of the move, defining interactions with target types.
            damage (int): The base damage value the move can deal.
            category (str): Either 'physical' or 'special' depending on the stat used.
            accuracy (int): Chance (0–100) for the move to hit the target.
            pp (int): Number of times the move can be used before depletion.
        """
        self.name = name
        self.element = element
        self.damage = damage
        self.damage_class = category  # 'physical' or 'special'
        self.accuracy = accuracy
        self.pp = pp
        self.priority = 0  # Default priority for the move

    # --- Factory Method ---

    @classmethod
    def from_csv_row(cls, row):
        """
        Create a Move object from a row of a CSV or DataFrame.

        This factory method parses typical move data from a CSV-formatted source,
        including automatic type conversion and formatting.

        Args:
            row (pd.Series): A pandas Series containing the following fields:
                - 'name' (str): The name of the move.
                - 'type' (str): Element type (e.g., 'Fire').
                - 'power' (int): Base damage value.
                - 'damage_class' (str): Category as a string ('physical' or 'special').
                - 'accuracy' (int): Hit chance from 0 to 100.
                - 'pp' (int): Number of usages.

        Returns:
            Move: A new instance of Move with properly parsed fields.
        """
        _power = row.get('power', None)
        try:
            damage = int(_power)
        except (TypeError, ValueError):
            damage = 0  # ou une autre valeur par défaut

        # accuracy (par défaut 100 si vide ou non convertible)
        _acc = row.get('accuracy', None)
        try:
            accuracy = int(_acc)
        except (TypeError, ValueError):
            accuracy = 100 # a modif car implique n'echoue jamais et ca fonctionne pas bien comme ca dcp

        return cls(
            name=row['name'],
            element=row['type'],
            damage=damage,
            category=row['damage_class'].lower(),  # normalize casing
            accuracy=accuracy,
            pp=int(row['pp']),
            priority=int(row.get('priority', 0)),  # Default to 0 if not present
        )
