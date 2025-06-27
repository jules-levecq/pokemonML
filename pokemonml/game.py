# game.py

import PySimpleGUI as sg
import pandas as pd
from pokemonml.create_pokemon import PokemonFactory
from pokemonml.damage import PokemonDamageCalculator
from pokemonml.right_move_machine import RightMoveMachine
from pokemonml.display import display_turn_summary
from pokemonml.config import POKEMON_CSV, MOVES_CSV, TYPE_CHART_CSV
from team_builder import load_teams

def simulate_battle():
    teams = load_teams()
    if len(teams) < 2:
        sg.popup_error("Il faut au moins 2 équipes pour simuler.")
        return

    # Choix des deux équipes
    layout = [
        [sg.Text("Équipe A:"), sg.Combo(list(teams.keys()), key='A')],
        [sg.Text("Équipe B:"), sg.Combo(list(teams.keys()), key='B')],
        [sg.Button("Lancer"), sg.Button("Annuler")]
    ]
    win = sg.Window("Sélection des équipes", layout)
    event, vals = win.read()
    win.close()
    if event != "Lancer":
        return

    teamA, teamB = vals['A'], vals['B']
    if teamA == teamB:
        sg.popup_error("Choisissez deux équipes différentes.")
        return

    # Pour l'exemple, on prend le premier Pokémon de chaque équipe
    factory = PokemonFactory(POKEMON_CSV, MOVES_CSV)
    dcalc   = PokemonDamageCalculator(TYPE_CHART_CSV, verbose=False)
    rmm     = RightMoveMachine(verbose=False)

    pA_name = teams[teamA][0]
    pB_name = teams[teamB][0]
    pA = factory.create_pokemon(pA_name, level=50)
    pB = factory.create_pokemon(pB_name, level=50)

    # Attribution automatique des moves (les 4 premiers du CSV)
    moves_df = pd.read_csv(MOVES_CSV)
    for name in moves_df['name'].iloc[:4]:
        factory.add_move_to_pokemon(pA, name)
        factory.add_move_to_pokemon(pB, name)

    # Simulation d'un tour
    pred = rmm.find_best_move(pA, pB)
    exec_ = dcalc.resolve_interaction(
        attacker=pA, defender=pB,
        move=pred.move, random_multiplier=False
    )

    # Affichage popup
    summary = f"{pred.attacker.name} utilise {pred.move.name} → dégâts={exec_.damage}"
    sg.popup("Résultat du tour", summary)

    # Optionnel : afficher dans la console détaillé
    display_turn_summary(pA, pB, pred, exec_)
