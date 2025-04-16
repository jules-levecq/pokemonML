from .damage import PokemonDamageCalculator, Attack
from .create_pokemon import PokemonFactory, Pokemon


class RightMoveMachine:
    """
    AI utility class for determining the optimal move in a Pokémon battle context.

    This class evaluates all available moves of a given Pokémon (the attacker) against a target (the defender),
    and returns the most effective one based on expected damage output. It uses a type chart and the same
    damage formulas as PokémonDamageCalculator to simulate theoretical attacks.

    Attributes:
        factory (PokemonFactory): Internal Pokémon factory for possible future extensions.
        damage_calculator (PokemonDamageCalculator): Core logic used to evaluate move effectiveness.
    """

    def __init__(self, csv_path: str, verbose=False):
        """
        Initialize the move recommender system with the path to the type effectiveness CSV.

        Args:
            csv_path (str): Path to the chart file defining type matchups (e.g., "data/chart.csv").
            verbose (bool): If True, enables verbose output from damage calculation.
        """
        self.factory = PokemonFactory('data/pokemon.csv', 'data/moves.csv')
        self.damage_calculator = PokemonDamageCalculator(csv_path, verbose=verbose)

    def find_best_move(self, attacker: Pokemon, defender: Pokemon) -> Attack:
        """
        Evaluate all available moves from the attacker and choose the best move based on the following criteria:
            1. First, consider only moves where compute_theoretical_attack returns an effective_damage 
            not equal to -1 (i.e. moves that will KO the defender).
            2. If one or more moves meet that criterion, select the move with the best accuracy.
            3. Otherwise, select the move that deals the highest minimum damage (using damage_range[0]).
        
        Args:
            attacker (Pokemon): The Pokémon executing the move.
            defender (Pokemon): The target Pokémon.

        Returns:
            Attack: The simulated attack result corresponding to the best move.
        
        Raises:
            ValueError: If the attacker has no available moves.
        """
        if not attacker.moves:
            raise ValueError(f"{attacker.name} has no available moves.")

        # Compute the theoretical attack result for each move.
        theoretical_attacks = [
            self.damage_calculator.compute_theoretical_attack(
                attacker, defender, move, is_crit=False,
                random_multiplier=self.damage_calculator.verbose
            )
            for move in attacker.moves
        ]

        # Filter moves that guarantee a KO (effective_damage != -1).
        guaranteed_moves = [atk for atk in theoretical_attacks if atk.effective_damage != -1]

        if guaranteed_moves:
            # If there are moves that guarantee a KO, choose the one with the highest accuracy.
            best_attack = max(guaranteed_moves, key=lambda atk: atk.move.accuracy)
        else:
            # Otherwise, choose the move with the highest minimum damage.
            best_attack = max(theoretical_attacks, key=lambda atk: atk.damage_range[0])

        return best_attack

    def find_best_move_name(self, attacker: Pokemon, defender: Pokemon) -> str:
        """
        Return only the name of the best move (most effective), rather than the full object.

        This method is useful when only the label or identifier of the move is needed,
        for example in command generation or display UI.

        Args:
            attacker (Pokemon): The attacking Pokémon.
            defender (Pokemon): The defending Pokémon.

        Returns:
            str: The name of the most effective move.

        Raises:
            ValueError: If the attacker has no moves available.
        """
        best_attack = self.find_best_move(attacker, defender)
        return best_attack.move.name  # type: ignore[attr-defined]
