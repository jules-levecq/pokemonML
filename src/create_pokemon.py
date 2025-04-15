import pandas as pd
from .utils import read_csv_data
from .stats import Stats
from .moves import Move
from copy import deepcopy


class Pokemon:
    """
    Class representing a Pokémon entity.

    Attributes:
        name (str): Name of the Pokémon.
        base_stats (Stats): The calculated base stats of the Pokémon.
        current_stats (Stats): The current stats which can change during battle.
        type1 (str): Primary type of the Pokémon.
        type2 (str or None): Secondary type if applicable.
        level (int): Pokémon's level.
        moves (list): List of moves (max 4).
    """

    def __init__(self, name, stats, type1, type2=None, level=50):
        """Initialize a Pokémon object with stats, types and level."""
        self.name = name
        self.base_stats = stats
        self.current_stats = deepcopy(stats)
        self.type1 = type1
        self.type2 = type2
        self.level = level
        self.moves = []

    # --- Factory ---

    @classmethod
    def from_csv_row(cls, row, level, stats: Stats):
        """Create a Pokémon instance from a row of the Pokémon CSV and precomputed stats."""
        return cls(
            name=row['Name'],
            stats=stats,
            type1=row['Type 1'],
            type2=row['Type 2'] if pd.notnull(row['Type 2']) else None,
            level=level
        )

    # --- Move Management ---

    def add_move(self, move):
        """Add a move to the Pokémon's list of moves (max 4)."""
        if len(self.moves) < 4:
            self.moves.append(move)
        else:
            raise Exception(f"{self.name} cannot have more than 4 moves.")

    # --- HP Management ---

    def take_damage(self, damage):
        """Reduce the Pokémon's current HP by the given damage."""
        self.current_stats.health = max(0, self.current_stats.health - damage)

    def heal(self, amount):
        """Heal the Pokémon by a certain amount, without exceeding base HP."""
        self.current_stats.health = min(self.base_stats.health, self.current_stats.health + amount)

    # --- Utility ---

    def reset_stats(self):
        """Reset current stats to base stats (e.g., after battle)."""
        self.current_stats = deepcopy(self.base_stats)

    def to_dict(self):
        """Return a dictionary representation of the Pokémon (useful for logging/export)."""
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
    Factory class to create Pokémon and moves from CSV data.

    Attributes:
        pokemon_data (pd.DataFrame): Raw data of Pokémon.
        moves_data (pd.DataFrame): Raw data of moves.
    """

    def __init__(self, pokemon_csv_path: str, moves_csv_path: str):
        """Load Pokémon and move data from given CSV file paths."""
        self.pokemon_data = read_csv_data(pokemon_csv_path)
        self.moves_data = read_csv_data(moves_csv_path)

    # --- Pokémon / Move Creation ---

    def create_pokemon(self, name: str, level):
        """Create a Pokémon instance by its name and level."""
        pokemon_row = self.pokemon_data[self.pokemon_data['Name'] == name].iloc[0]
        stats = Stats.from_csv_row(pokemon_row, level)
        return Pokemon.from_csv_row(pokemon_row, level, stats)

    def create_move(self, name: str):
        """Create a Move instance from the move name."""
        move_row = self.moves_data[self.moves_data['name'] == name].iloc[0]
        return Move.from_csv_row(move_row)

    # --- Move Assignment ---

    def add_move_to_pokemon(self, pokemon: Pokemon, move_name: str):
        """Assign a move to a given Pokémon by move name."""
        move = self.create_move(move_name)
        pokemon.add_move(move)
