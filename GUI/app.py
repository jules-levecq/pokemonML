# Import de Streamlit pour l'interface
import streamlit as st

# Import de tes modules métier
from pokemonml.create_pokemon import PokemonFactory
from pokemonml.right_move_machine import RightMoveMachine
from pokemonml.display import display_turn_summary

# Pour capturer le texte que display_turn_summary imprime
from io import StringIO

# ─── Initialisation ───────────────────────────────────────────────────────────

# Chargement des données de Pokémon et de mouvements
factory = PokemonFactory()
# Moteur pour choisir le meilleur coup d'attaque
rmm = RightMoveMachine()

# Récupération de la liste des noms de Pokémon (unique) pour les menus déroulants
noms = list(factory.pokemon_data['Name'].unique())

# ─── Widgets d'entrée ──────────────────────────────────────────────────────────

# Choix du Pokémon attaquant via un selectbox (par défaut Pikachu si présent)
atk_name = st.selectbox(
    "Pokémon Attaquant",
    noms,
    index=noms.index("Pikachu") if "Pikachu" in noms else 0
)

# Choix du niveau de l'attaquant via un slider (1–100, défaut 50)
atk_lvl = st.slider("Niveau Attaquant", 1, 100, 50)

# Choix du Pokémon défenseur de la même manière
def_name = st.selectbox(
    "Pokémon Défenseur",
    noms,
    index=noms.index("Bulbasaur") if "Bulbasaur" in noms else 0
)
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
