from pokemon_dammage_calculator import Pokemon, Stats, Move
import pandas as pd

# Création d'un Pokémon en utilisant les données du CSV

def create_pokemon(name: str, pokemon_data):
    pokemon_row = pokemon_data[pokemon_data['Name'] == name].iloc[0]
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
        moves=[],  # vide au début, à remplir ensuite
        type1=pokemon_row['Type 1'],
        type2=pokemon_row['Type 2'] if pd.notnull(pokemon_row['Type 2']) else None,
        level=50  # Niveau par défaut
    )
    return pokemon

# Création d'une attaque en utilisant les données du CSV

def create_move(name: str, moves_data):
    move_row = moves_data[moves_data['Name'] == name].iloc[0]
    move = Move(
        name=name,
        element=move_row['Type'],
        damage=int(move_row['Power']),
        category=move_row['Category'].lower(),
        accuracy=int(move_row['Accuracy'])
    )
    return move

# Ajouter une attaque à un Pokémon
def add_move_to_pokemon(pokemon, move):
    if len(pokemon.moves) < 4:  # Limitation habituelle à 4 attaques par Pokémon
        pokemon.moves.append(move)
    else:
        raise Exception(f"{pokemon.name} ne peut pas avoir plus de 4 attaques.")
