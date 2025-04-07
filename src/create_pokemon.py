import pandas as pd
from .utils import read_csv_data
from .stats import Stats
from .moves import Move


class Pokemon:
    """Class representing a Pokémon entity."""
    def __init__(self, name, stats, type1, type2=None, level=50):
        """
        Initialize a Pokémon.
        :param name: Name of the Pokémon
        :param stats: Stats object
        :param type1: Primary type
        :param type2: Secondary type (optional)
        :param level: Level of the Pokémon (default 50)
        """
        self.name = name
        self.base_stats = stats
        self.current_stats = stats.clone()
        self.type1 = type1
        self.type2 = type2
        self.level = level
        self.moves = []

    def add_move(self, move):
        """Add a move to the Pokémon's move list (max 4 moves)."""
        if len(self.moves) < 4:
            self.moves.append(move)
        else:
            raise Exception(f"{self.name} cannot have more than 4 moves.")


class PokemonFactory:
    """Factory class to create Pokémon and moves from CSV data."""
    def __init__(self, pokemon_csv_path: str, moves_csv_path: str):
        """
        Load Pokémon and move data from CSV files.
        :param pokemon_csv_path: Path to the Pokémon data CSV
        :param moves_csv_path: Path to the move data CSV
        """
        self.pokemon_data = read_csv_data(pokemon_csv_path)
        self.moves_data = read_csv_data(moves_csv_path)

    def create_pokemon(self, name: str):
        """
        Create a Pokémon instance by name.
        :param name: Name of the Pokémon
        :return: A new Pokémon object
        """
        pokemon_row = self.pokemon_data[self.pokemon_data['Name'] == name].iloc[0]
        stats = Stats(
            health=int(pokemon_row['HP']),
            attack=int(pokemon_row['Attack']),
            defense=int(pokemon_row['Defense']),
            attack_spe=int(pokemon_row['Sp. Atk']),
            defense_spe=int(pokemon_row['Sp. Def']),
            speed=int(pokemon_row['Speed'])
        )

        pokemon = Pokemon(
            name=name,
            stats=stats,
            type1=pokemon_row['Type 1'],
            type2=pokemon_row['Type 2'] if pd.notnull(pokemon_row['Type 2']) else None,
            level=50
        )
        return pokemon

    def create_move(self, name: str):
        """
        Create a Move instance by name.
        :param name: Name of the move
        :return: A new Move object
        """
        move_row = self.moves_data[self.moves_data['name'] == name].iloc[0]
        move = Move(
            name=name,
            element=move_row['type'],
            damage=int(move_row['power']),
            category=move_row['damage_class'].lower(),
            accuracy=int(move_row['accuracy'])
        )
        return move

    def add_move_to_pokemon(self, pokemon: Pokemon, move_name: str):
        """
        Add a move to a Pokémon by name.
        :param pokemon: The Pokémon instance
        :param move_name: Name of the move to add
        """
        move = self.create_move(move_name)
        pokemon.add_move(move)

    def get_pokemon_data(self):
        """Return the raw Pokémon DataFrame."""
        return self.pokemon_data

    def get_moves_data(self):
        """Return the raw moves DataFrame."""
        return self.moves_data
