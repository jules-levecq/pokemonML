import streamlit as st
import pandas as pd
import contextlib

from pokemonml.create_pokemon import PokemonFactory
from pokemonml.right_move_machine import RightMoveMachine
from pokemonml.display import display_turn_summary
from pokemonml.config import DATA_DIR

from io import StringIO

# ─── Initialisation ───────────────────────────────────────────────────────────

factory = PokemonFactory()
rmm = RightMoveMachine()

pokemon_df = factory.pokemon_data      # DataFrame des Pokémons (colonnes id, Name, etc.)
moves_df = factory.moves_data        # DataFrame des mouvements (colonnes id, name, etc.)


@st.cache_data
def load_learn_data():
    return pd.read_csv(DATA_DIR / 'pokemonMovesCanLearn.csv')


learn_df = load_learn_data()

noms = list(factory.pokemon_data['Name'].unique())

# ─── Widget premier Joueur ──────────────────────────────────────────────────────────

atk_name = st.selectbox(
    "Pokémon Attaquant",
    noms,
    index=noms.index("Pikachu") if "Pikachu" in noms else 0
)

atk_pkm_row = pokemon_df[pokemon_df['Name'] == atk_name].iloc[0]
atk_pkm_id = atk_pkm_row['Id']

atk_possible_move_ids = learn_df.loc[
    learn_df['pokemon_id'] == atk_pkm_id,
    'move_id'
].unique()

atk_possible_moves = (
    factory.moves_data
    .loc[factory.moves_data['id'].isin(atk_possible_move_ids), 'name']
    .sort_values()
    .tolist()
)

for i in range(4):
    key = f"atk{i+1}"
    if key not in st.session_state:
        st.session_state[key] = atk_possible_moves[i] if i < len(atk_possible_moves) else atk_possible_moves[0]

cols = st.columns(4)
atk_selected_moves = []
for i, col in enumerate(cols, start=1):
    key = f"atk{i}"

    opts = [mv for mv in atk_possible_moves if mv not in atk_selected_moves]
    opts.append(st.session_state[key])
    opts = sorted(opts, key=lambda x: atk_possible_moves.index(x))

    choice = col.selectbox(
        f"Attaque {i}",
        options=opts,
        index=opts.index(st.session_state[key]),
        key=key
    )
    atk_selected_moves.append(choice)

atk_lvl = st.slider("Niveau Attaquant", 1, 100, 50)

# ─── Widget deuxieme Joueur ──────────────────────────────────────────────────────────

def_name = st.selectbox(
    "Pokémon Défenseur",
    noms,
    index=noms.index("Bulbasaur") if "Bulbasaur" in noms else 0
)

def_pkm_row = pokemon_df[pokemon_df['Name'] == def_name].iloc[0]
def_pkm_id = def_pkm_row['Id']

def_possible_move_ids = learn_df.loc[
    learn_df['pokemon_id'] == def_pkm_id,
    'move_id'
].unique()

def_possible_moves = (
    factory.moves_data
    .loc[factory.moves_data['id'].isin(def_possible_move_ids), 'name']
    .sort_values()
    .tolist()
)

for i in range(4):
    key = f"def{i+1}"
    if key not in st.session_state:
        st.session_state[key] = def_possible_moves[i] if i < len(def_possible_moves) else def_possible_moves[0]

cols = st.columns(4)
def_selected_moves = []
for i, col in enumerate(cols, start=1):
    key = f"def{i}"

    opts = [mv for mv in def_possible_moves if mv not in def_selected_moves]
    opts.append(st.session_state[key])
    opts = sorted(opts, key=lambda x: def_possible_moves.index(x))

    choice = col.selectbox(
        f"Attaque {i}",
        options=opts,
        index=opts.index(st.session_state[key]),
        key=key
    )
    def_selected_moves.append(choice)

def_lvl = st.slider("Niveau Défenseur", 1, 100, 50)

# ─── Bouton d'action ───────────────────────────────────────────────────────────

if st.button("Calculer meilleur coup"):
    atk = factory.create_pokemon(atk_name, atk_lvl)
    defn = factory.create_pokemon(def_name, def_lvl)

    # Ajout des mouvements sélectionnés
    for mv in atk_selected_moves:
        factory.add_move_to_pokemon(atk, mv)
    for mv in def_selected_moves:
        factory.add_move_to_pokemon(defn, mv)

    # Meilleur coup theorique
    best = rmm.find_best_move(atk, defn)

    # Capture textuelle
    buf = StringIO()
    with contextlib.redirect_stdout(buf):
        display_turn_summary(atk, defn, best, best)

    # Affichage résultat
    st.subheader(f"Meilleur coup → {best.move.name}")
    st.text(buf.getvalue())
