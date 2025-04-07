from pokemon_dammage_calculator import PokemonDamageCalculator, Attack
from create_pokemon import PokemonFactory, Stats, Move, Pokemon

class RightMoveMachine:
    def __init__(self, csv_path: str):
        """
        Initialize the RightMoveMachine with a CSV path for type effectiveness chart.

        :param csv_path: Path to the CSV file containing type effectiveness data.
        """
        self.factory = PokemonFactory('data/pokemon.csv', 'data/moves.csv')
        self.damage_calculator = PokemonDamageCalculator(csv_path)

    @staticmethod
    def find_best_move(attacker: Pokemon, defender: Pokemon) -> Attack:
        """
        Find the best move for the attacker against the defender.

        :param attacker: The attacking Pokémon.
        :param defender: The defending Pokémon.
        :return: The best attack result.
        """
        best_attack = None

        #initialize damage calculator beacause it is a static method
        damage_calculator = PokemonDamageCalculator('data/chart.csv')

        for move in attacker.moves:
            attack_result = damage_calculator.calculate_damage(attacker, defender, move)

            # Check if this is the first attack or if it's better than the current best by checking the average of the damage range
            if best_attack is None or (attack_result.damage_range[0] + attack_result.damage_range[1]) / 2 > (
                    best_attack.damage_range[0] + best_attack.damage_range[1]) / 2:
                best_attack = attack_result

        return best_attack

    