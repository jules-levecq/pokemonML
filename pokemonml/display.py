from .damage import Attack
from .create_pokemon import Pokemon


def display_turn_summary(attacker: Pokemon, defender: Pokemon, predicted_attack: Attack, executed_attack: Attack) -> None:
    """
    Print a detailed summary of a single battle turn, including:
    - The predicted best move.
    - The move that was actually executed.
    - Whether it hit or missed.
    - Damage dealt, critical hit status, and effectiveness.
    - HP state after the turn.

    Args:
        attacker (Pokemon): The Pokémon that performed the attack.
        defender (Pokemon): The Pokémon that was attacked.
        predicted_attack (Attack): The best move predicted before the turn.
        executed_attack (Attack): The actual move executed and its result.
    """
    print("\n" + "=" * 60)
    print("Pre-Turn Prediction")
    print("-" * 60)
    print(f"Expected best move: {predicted_attack.move.name} (PP: {predicted_attack.move.pp})")
    print(f"→ Estimated Damage: {predicted_attack.effective_damage:.2f}")
    print(f"→ Effectiveness: x{predicted_attack.effectiveness:.2f}")
    print("=" * 60)

    print("Turn Execution")
    print("-" * 60)
    print(f"{attacker.name} uses {executed_attack.move.name} (PP left: {executed_attack.move.pp})")
    if executed_attack.missed:
        print("→ The move missed!")
    else:
        print(f"→ Deals {executed_attack.effective_damage:.2f} damage to {defender.name}")
        if executed_attack.crit:
            print("→ It's a critical hit!")
        print(f"→ Effectiveness: x{executed_attack.effectiveness:.2f}")
    print("=" * 60)

    print("Post-Turn Status")
    print("-" * 60)
    print(f"{defender.name}'s HP: {round(defender.current_stats.health)} / {defender.base_stats.health}")
    print("=" * 60 + "\n")
