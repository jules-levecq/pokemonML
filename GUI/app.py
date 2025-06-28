# Import de Streamlit pour l'interface
import streamlit as st
import pandas as pd

# Import de tes modules métier
from pokemonml.create_pokemon import PokemonFactory
from pokemonml.right_move_machine import RightMoveMachine
from pokemonml.display import display_turn_summary
from pokemonml.config import DATA_DIR

# Pour capturer le texte que display_turn_summary imprime
from io import StringIO

# ─── Initialisation ───────────────────────────────────────────────────────────

# Chargement des données de Pokémon et de mouvements
factory = PokemonFactory()
# Moteur pour choisir le meilleur coup d'attaque
rmm = RightMoveMachine()

pokemon_df = factory.pokemon_data      # DataFrame des Pokémons (colonnes id, Name, etc.)
moves_df = factory.moves_data        # DataFrame des mouvements (colonnes id, name, etc.)


@st.cache_data
def load_learn_data():
    return pd.read_csv(DATA_DIR / 'pokemonMovesCanLearn.csv')


learn_df = load_learn_data()

# Récupération de la liste des noms de Pokémon (unique) pour les menus déroulants
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

# Quatre selectbox pour choisir jusqu'à 4 attaques différentes
cols = st.columns(4)

# Dans chaque colonne, on place un selectbox
with cols[0]:
    atk_move1 = st.selectbox("Attaque 1", options=atk_possible_moves, index=0)

with cols[1]:
    atk_move2 = st.selectbox("Attaque 2", options=atk_possible_moves, index=1 if len(atk_possible_moves)>1 else 0)

with cols[2]:
    atk_move3 = st.selectbox("Attaque 3", options=atk_possible_moves, index=2 if len(atk_possible_moves)>2 else 0)

with cols[3]:
    atk_move4 = st.selectbox("Attaque 4", options=atk_possible_moves, index=3 if len(atk_possible_moves)>3 else 0)

selected_moves = [atk_move1, atk_move2, atk_move3, atk_move4]

# Choix du niveau de l'attaquant via un slider (1–100, défaut 50)
atk_lvl = st.slider("Niveau Attaquant", 1, 100, 50)

# ─── Widget deuxieme Joueur ──────────────────────────────────────────────────────────

# Choix du Pokémon défenseur de la même manière
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

# Quatre selectbox pour choisir jusqu'à 4 attaques différentes
cols = st.columns(4)

# Dans chaque colonne, on place un selectbox
with cols[0]:
    def_move1 = st.selectbox("Attaque 1", options=def_possible_moves, index=0)

with cols[1]:
    def_move2 = st.selectbox("Attaque 2", options=def_possible_moves, index=1 if len(def_possible_moves)>1 else 0)

with cols[2]:
    def_move3 = st.selectbox("Attaque 3", options=def_possible_moves, index=2 if len(def_possible_moves)>2 else 0)

with cols[3]:
    def_move4 = st.selectbox("Attaque 4", options=def_possible_moves, index=3 if len(def_possible_moves)>3 else 0)

selected_moves = [def_move1, def_move2, def_move3, def_move4]

def_lvl = st.slider("Niveau Défenseur", 1, 100, 50)

# ─── Bouton d'action ───────────────────────────────────────────────────────────

# Ce bloc ne s'exécute que lorsque l'utilisateur clique sur le bouton
if st.button("Calculer meilleur coup"):
    # 1) Création des instances de Pokémon selon les sélections
    atk = factory.create_pokemon(atk_name, atk_lvl)
    defn = factory.create_pokemon(def_name, def_lvl)

    # 2) Attribution des mouvements à l'attaquant
    #    Ici on prend arbitrairement les 4 premiers moves du CSV
    for move_name in factory.moves_data['name'].head(4):
        factory.add_move_to_pokemon(atk, move_name)

    # 3) Calcul du meilleur coup face au défenseur
    best = rmm.find_best_move(atk, defn)

    # 4) Préparation à l'affichage du détail du tour
    #    On redirige temporairement `stdout` dans un buffer pour capturer les print()
    buf = StringIO()
    old_stdout = sys.stdout
    sys.stdout = buf

    # 5) Affichage "cli" du résumé de tour dans le buffer
    display_turn_summary(atk, defn, best, best)

    # 6) On restaure stdout
    sys.stdout = old_stdout

    # 7) Affichage dans l'app Streamlit :
    #    - Un titre indiquant le coup choisi
    #    - Le texte complet du résumé de tour
    st.subheader(f"Meilleur coup → {best.move.name}")
    st.text(buf.getvalue())
