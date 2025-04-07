
from pokemon_dammage_calculator import PokemonDamageCalculator, Attack
from utils import read_csv_data, display_damage_result
from dataclasses import dataclass
from create_pokemon import PokemonFactory

class RightMoveMachine:
    def __init__(self, csv_path: str):
        """
        Initialize the RightMoveMachine with a CSV path for type effectiveness chart.

        :param csv_path: Path to the CSV file containing type effectiveness data.
        """
        self.factory = PokemonFactory('data/pokemon.csv', 'data/moves.csv')
        self.damage_calculator = PokemonDamageCalculator(csv_path)

    