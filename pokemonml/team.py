class Team:
    def __init__(self, pokemons: list, name="player"):
        self.name = name
        self.pokemons = pokemons  # Liste de Pokémon (ex: instances de class `Pokemon`)
        self.active_index = 0     # Index du Pokémon actuellement en combat

    @property
    def active_pokemon(self):
        return self.pokemons[self.active_index]

    def is_defeated(self):
        return all(p.is_fainted() for p in self.pokemons)

    def get_available_switches(self):
        return [i for i, p in enumerate(self.pokemons)
                if i != self.active_index and not p.is_fainted()]

    def switch_to(self, index):
        if index == self.active_index:
            raise ValueError("Already active")
        if self.pokemons[index].is_fainted():
            raise ValueError("Cannot switch to a fainted Pokémon")
        print(f"{self.name} switched from {self.active_pokemon.name} to {self.pokemons[index].name}")
        self.active_index = index

    def __repr__(self):
        return f"Team({[p.name for p in self.pokemons]}, active={self.active_pokemon.name})"
