import pandas as pd
from .data_loader import read_csv_data


class Stats:
    def __init__(self, health, attack, defense, attack_spe, defense_spe, speed):
        self.health = health
        self.attack = attack
        self.defense = defense
        self.attack_spe = attack_spe
        self.defense_spe = defense_spe
        self.speed = speed


class Move:
    def __init__(self, name, element, damage, category, accuracy):
        self.name = name
        self.element = element
        self.damage = damage
        self.damage_class = category  # "physical" ou "special"
        self.accuracy = accuracy


class Pokemon:
    def __init__(self, name, stats, type1, type2=None, level=50):
        self.name = name
        self.stats = stats
        self.type1 = type1
        self.type2 = type2
        self.level = level
        self.moves = []

    def add_move(self, move):
        if len(self.moves) < 4:
            self.moves.append(move)
        else:
            raise Exception(f"{self.name} ne peut pas avoir plus de 4 attaques.")


class PokemonFactory:
    def __init__(self, pokemon_csv_path: str, moves_csv_path: str):
        self.pokemon_data = read_csv_data(pokemon_csv_path)
        self.moves_data = read_csv_data(moves_csv_path)

    def create_pokemon(self, name: str):
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
        move = self.create_move(move_name)
        pokemon.add_move(move)

    def get_pokemon_data(self):
        return self.pokemon_data

    def get_moves_data(self):
        return self.moves_data
