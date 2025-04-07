
from pokemon_dammage_calculator import PokemonDamageCalculator, Attack
from utils import read_csv_data, display_damage_result
from dataclasses import dataclass
from create_pokemon import PokemonFactory, Stats, Move, Pokemon

class RightMoveMachine:
    def __init__(self, csv_path: str):
        """
        Initialize the RightMoveMachine with a CSV path for type effectiveness chart.

        :param csv_path: Path to the CSV file containing type effectiveness data.
        """
        self.factory = PokemonFactory('data/pokemon.csv', 'data/moves.csv')
        self.damage_calculator = PokemonDamageCalculator(csv_path)

    def find_best_move(self, attacker: Pokemon, defender: Pokemon) -> Attack:
        """
        Find the best move for the attacker against the defender.

        :param attacker: The attacking Pokémon.
        :param defender: The defending Pokémon.
        :return: The best attack result.
        """
        best_attack = None

        for move in attacker.moves:
            attack_result = self.damage_calculator.calculate_damage(attacker, defender, move)

            if not best_attack or attack_result.effective_damage > best_attack.effective_damage:
                best_attack = attack_result

        return best_attack
