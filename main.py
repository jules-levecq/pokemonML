from src.create_pokemon import PokemonFactory
from src.pokemon_dammage_calculator import PokemonDamageCalculator
from src.right_move_machine import RightMoveMachine
from src.utils import display_damage_result


# Initialize the factory and the damage calculator
factory = PokemonFactory('data/pokemon.csv', 'data/moves.csv')
damage_calculator = PokemonDamageCalculator('data/chart.csv')

# Create Pokémon
pikachu = factory.create_pokemon("Pikachu")
bulbasaur = factory.create_pokemon("Bulbasaur")

# Add moves
factory.add_move_to_pokemon(pikachu, "Thunder")
factory.add_move_to_pokemon(pikachu, "Quick Attack")
factory.add_move_to_pokemon(pikachu, "Iron Tail")
factory.add_move_to_pokemon(pikachu, "Volt Tackle")
factory.add_move_to_pokemon(bulbasaur, "Vine Whip")


list_attack = []
# Calculate damage
for i in range(50) :
    damage = damage_calculator.calculate_damage(pikachu, bulbasaur, pikachu.moves[0])
    # Display the result
    display_damage_result(pikachu, bulbasaur, pikachu.moves[0], damage)

    # Store the damage in a list
    list_attack.append(damage)

    # Si c'est un coup critique, on arrête la boucle
    if damage.crit:
        print("Critical hit achieved! Ending simulation. At the step", i + 1)
        break

#find the best move
best_attack = RightMoveMachine.find_best_move(pikachu, bulbasaur)
display_damage_result(pikachu, bulbasaur, best_attack.move, best_attack)