# battle.py

import random
from .right_move_machine import RightMoveMachine
from .create_pokemon import Pokemon
# from .moves import Move


class BattleSimulator:
    def __init__(self):
        self.rmm = RightMoveMachine()

    def full_turn_interaction(self, pokemon1: Pokemon, pokemon2: Pokemon, random_multiplier: bool = True) -> tuple[tuple, tuple | None]:
        """
        Retourne deux tuples :
          - first_half_turn  = (attacker, defender, move, result)
          - second_half_turn = idem
        """
        from .damage import PokemonDamageCalculator
        pdc = PokemonDamageCalculator()
        # on récupère les meilleurs moves prédits
        best1 = self.rmm.find_best_move(attacker=pokemon1, defender=pokemon2).move
        best2 = self.rmm.find_best_move(attacker=pokemon2, defender=pokemon1).move

        # on décide de l'ordre selon (priority, speed, random)
        score1 = (best1.priority, pokemon1.current_stats.speed, random.random())
        score2 = (best2.priority, pokemon2.current_stats.speed, random.random())

        if score1 >= score2:
            atk, defn, mv = pokemon1, pokemon2, best1
        else:
            atk, defn, mv = pokemon2, pokemon1, best2

        # on résout la première interaction
        first = (atk, defn, mv, pdc.resolve_interaction(attacker=atk, defender=defn, move=mv, random_multiplier=random_multiplier))

        # si le défenseur est toujours debout, on fait le deuxième demi-tour
        if defn.current_stats.health > 0:
            # on inverse attaquant et défenseur, on choisi l'autre move
            atk2 = pokemon2 if atk is pokemon1 else pokemon1
            mv2 = best2 if mv is best1 else best1
            defn2 = pokemon2 if defn is pokemon1 else pokemon1
            second = (atk2, defn2, mv2, pdc.resolve_interaction(attacker=atk2, defender=defn2, move=mv2, random_multiplier=random_multiplier))
        else:
            # KO direct
            return first, None

        return first, second
