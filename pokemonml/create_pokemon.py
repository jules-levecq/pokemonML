import pandas as pd
from .config import POKEMON_CSV, MOVES_CSV
from .utils import read_csv_data
from .stats import Stats
from .moves import Move
from copy import deepcopy


class Pokemon:
    """
    Represents a Pokémon entity in battle or training context.

    This class encapsulates the attributes and behavior of a Pokémon,
    including type, level, statistics (base and current), and moveset.

    Attributes:
        name (str): The name of the Pokémon (e.g., "Pikachu").
        base_stats (Stats): Computed stats based on level, base values, IVs, and EVs.
        current_stats (Stats): Mutable stats that change during battle (e.g., HP loss).
        type1 (str): Primary elemental type (e.g., "Electric").
        type2 (str | None): Optional secondary type.
        level (int): Level of the Pokémon.
        moves (list[Move]): List of up to 4 moves.
    """

    def __init__(self, name, stats, type1, type2=None, level=50):
        """
        Initialize a Pokémon object.

        Args:
            name (str): The Pokémon's name.
            stats (Stats): The Pokémon's base stats (computed beforehand).
            type1 (str): The primary type.
            type2 (str, optional): Secondary type, if applicable. Defaults to None.
            level (int, optional): The level of the Pokémon. Defaults to 50.
        """
        self.name = name
        self.base_stats = stats
        self.current_stats = deepcopy(stats)
        self.type1 = type1
        self.type2 = type2
        self.level = level
        self.moves = []

    # --- Factory constructor ---

    @classmethod
    def from_csv_row(cls, row, level, stats: Stats):
        """
        Create a Pokémon instance from a row of a DataFrame and a precomputed Stats object.

        Args:
            row (pd.Series): The row from the Pokémon CSV containing its attributes.
            level (int): The Pokémon's level.
            stats (Stats): A Stats object, computed using the same row and level.

        Returns:
            Pokemon: Instantiated Pokémon object.
        """
        return cls(
            name=row['Name'],
            stats=stats,
            type1=row['Type 1'],
            type2=row['Type 2'] if pd.notnull(row['Type 2']) else None,
            level=level
        )

    # --- Move Management ---

    def add_move(self, move):
        """
        Add a move to the Pokémon’s moveset, limited to 4.

        Args:
            move (Move): The move object to be added.

        Raises:
            Exception: If the Pokémon already has 4 moves.
        """
        if len(self.moves) < 4:
            self.moves.append(move)
        else:
            raise Exception(f"{self.name} cannot have more than 4 moves.")

    # --- HP and Healing ---

    def take_damage(self, damage):
        """
        Apply damage to the Pokémon's current HP.

        Args:
            damage (float | int): Amount of damage to subtract from current HP.
        """
        self.current_stats.health = max(0, self.current_stats.health - damage)

    def heal(self, amount):
        """
        Restore health to the Pokémon without exceeding its max HP.

        Args:
            amount (float | int): Amount of HP to restore.
        """
        self.current_stats.health = min(self.base_stats.health, self.current_stats.health + amount)

    # --- Utility methods ---

    def reset_stats(self):
        """
        Reset current stats to their original base values.
        Typically called after a battle.
        """
        self.current_stats = deepcopy(self.base_stats)

    def to_dict(self):
        """
        Return a serializable dictionary representation of the Pokémon.

        Useful for logging, display, or JSON export.

        Returns:
            dict: Key information about the Pokémon's state.
        """
        return {
            "name": self.name,
            "level": self.level,
            "type1": self.type1,
            "type2": self.type2,
            "hp": self.current_stats.health,
            "moves": [move.name for move in self.moves]
        }


class PokemonFactory:
    """
    Factory class for constructing Pokémon and Moves from structured CSV data.

    This class abstracts away the logic of reading and parsing raw CSV data
    into usable in-game objects like Pokémon and their moves.

    Attributes:
        pokemon_data (pd.DataFrame): DataFrame containing Pokémon base stats.
        moves_data (pd.DataFrame): DataFrame containing move definitions.
    """

    def __init__(self, pokemon_csv_path: str = POKEMON_CSV, moves_csv_path: str = MOVES_CSV):
        """
        Initialize the factory with Pokémon and move data loaded from CSV files.

        Args:
            pokemon_csv_path (str): Path to the Pokémon CSV file.
            moves_csv_path (str): Path to the moves CSV file.
        """
        self.pokemon_data = read_csv_data(pokemon_csv_path)
        self.moves_data = read_csv_data(moves_csv_path)

    # --- Pokémon / Move Creation ---

    def create_pokemon(self, name: str, level):
        """
        Create a Pokémon by its name and level.

        This includes computing its stats based on level and assigning types.

        Args:
            name (str): Name of the Pokémon to instantiate.
            level (int): Desired level of the Pokémon.

        Returns:
            Pokemon: Fully initialized Pokémon object.
        """
        pokemon_row = self.pokemon_data[self.pokemon_data['Name'] == name].iloc[0]
        stats = Stats.from_csv_row(pokemon_row, level)
        return Pokemon.from_csv_row(pokemon_row, level, stats)

    def create_move(self, name: str):
        """
        Create a Move instance by name.

        Args:
            name (str): Name of the move to instantiate.

        Returns:
            Move: A new Move object.
        """
        move_row = self.moves_data[self.moves_data['name'] == name].iloc[0]
        return Move.from_csv_row(move_row)

    # --- Assign Moves ---

    def add_move_to_pokemon(self, pokemon: Pokemon, move_name: str):
        """
        Assign a move to a Pokémon, by move name.

        Args:
            pokemon (Pokemon): The Pokémon to which the move should be added.
            move_name (str): The name of the move to assign.
        """
        move = self.create_move(move_name)
        pokemon.add_move(move)
