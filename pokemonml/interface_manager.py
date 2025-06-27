# interface_manager.py

import PySimpleGUI as sg

from team_builder import (
    load_pokemon_list, load_moves_list,
    load_teams, add_team, delete_team
)
from game import simulate_battle

def team_builder_window():
    pokemons = load_pokemon_list()
    layout = [
        [sg.Text("Nom de l'équipe:"), sg.Input(key='team_name')],
        [sg.Text("Sélectionnez (jusqu'à) 6 Pokémon:")],
        [sg.Listbox(pokemons, select_mode=sg.SELECT_MODE_MULTIPLE, size=(25,6), key='members')],
        [sg.Button("Créer / Mettre à jour"), sg.Button("Annuler")]
    ]
    window = sg.Window("Création d'équipe", layout)
    event, values = window.read()
    window.close()
    if event == "Créer / Mettre à jour":
        name = values['team_name'].strip()
        members = values['members']
        if not name:
            sg.popup_error("Donnez un nom à l'équipe.")
        elif not members:
            sg.popup_error("Sélectionnez au moins un Pokémon.")
        else:
            add_team(name, members)
            sg.popup("Équipe enregistrée !")

def team_manager_window():
    teams = load_teams()
    layout = [
        [sg.Text("Équipes existantes:")],
        [sg.Listbox(list(teams.keys()), size=(25,6), key='team_list')],
        [sg.Button("Supprimer"), sg.Button("Fermer")]
    ]
    window = sg.Window("Gestion des équipes", layout)
    event, values = window.read()
    window.close()
    if event == "Supprimer":
        sel = values['team_list']
        if sel:
            delete_team(sel[0])
            sg.popup(f"Équipe '{sel[0]}' supprimée.")

def main_window():
    layout = [
        [sg.Button("Créer une équipe"), sg.Button("Gérer les équipes"), sg.Button("Simuler un combat")],
        [sg.Button("Quitter")]
    ]
    window = sg.Window("Pokémon Simulateur", layout, element_justification='c')
    while True:
        event, _ = window.read()
        if event in (sg.WIN_CLOSED, "Quitter"):
            break
        elif event == "Créer une équipe":
            team_builder_window()
        elif event == "Gérer les équipes":
            team_manager_window()
        elif event == "Simuler un combat":
            simulate_battle()
    window.close()

if __name__ == "__main__":
    main_window()
