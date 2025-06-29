import streamlit as st
import pandas as pd
import random
import time
from copy import deepcopy

from pokemonml.create_pokemon import PokemonFactory
from pokemonml.right_move_machine import RightMoveMachine
from pokemonml.damage import PokemonDamageCalculator
from pokemonml.display import display_streamlit_battle_summary
from pokemonml.config import DATA_DIR, TYPE_CHART_CSV, POKEMON_CSV, MOVES_CSV
from pokemonml.team import Team

# ═══════════════════════════════════════════════════════════════════════════════
# 🎮 SIMULATEUR DE COMBAT POKÉMON COMPLET
# ═══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="🔥 Simulateur de Combat Pokémon",
    page_icon="⚔️",
    layout="wide"
)

st.title("⚔️ Simulateur de Combat Pokémon Complet")
st.markdown("---")

# ─── Initialisation des composants ───────────────────────────────────────────

@st.cache_resource
def initialize_components():
    """Initialise les composants du simulateur de combat."""
    factory = PokemonFactory(POKEMON_CSV, MOVES_CSV)
    rmm = RightMoveMachine(verbose=False)
    pdc = PokemonDamageCalculator(TYPE_CHART_CSV, verbose=False)
    return factory, rmm, pdc

factory, rmm, pdc = initialize_components()

@st.cache_data
def load_learn_data():
    """Charge les données des mouvements que peuvent apprendre les Pokémon."""
    return pd.read_csv(DATA_DIR / 'pokemonMovesCanLearn.csv')

learn_df = load_learn_data()
pokemon_df = factory.pokemon_data
moves_df = factory.moves_data
noms = list(pokemon_df['Name'].unique())

# ─── Configuration du combat ──────────────────────────────────────────────────

st.header("🎯 Configuration du Combat")

col1, col2 = st.columns(2)

# ═══ ÉQUIPE 1 ═══
with col1:
    st.subheader("🔵 Équipe 1 (Joueur)")
    
    # Sélection du nombre de Pokémon
    nb_pokemon_1 = st.selectbox(
        "Nombre de Pokémon",
        [1, 2, 3, 4, 5, 6],
        index=0,
        key="nb_pokemon_1"
    )
    
    team1_pokemon = []
    for i in range(nb_pokemon_1):
        with st.expander(f"Pokémon {i+1}", expanded=(i == 0)):
            # Sélection du Pokémon
            pokemon_name = st.selectbox(
                f"Pokémon {i+1}",
                noms,
                index=noms.index("Pikachu") if "Pikachu" in noms and i == 0 else i % len(noms),
                key=f"team1_pokemon_{i}"
            )
            
            # Niveau
            level = st.slider(
                f"Niveau",
                1, 100, 50,
                key=f"team1_level_{i}"
            )
            
            # Sélection des mouvements
            pokemon_row = pokemon_df[pokemon_df['Name'] == pokemon_name].iloc[0]
            pokemon_id = pokemon_row['Id']
            
            possible_move_ids = learn_df.loc[
                learn_df['pokemon_id'] == pokemon_id,
                'move_id'
            ].unique()
            
            possible_moves = (
                moves_df
                .loc[moves_df['id'].isin(possible_move_ids), 'name']
                .sort_values()
                .tolist()
            )
            
            selected_moves = []
            for j in range(4):
                available_moves = [mv for mv in possible_moves if mv not in selected_moves]
                if not available_moves:
                    available_moves = possible_moves
                
                move = st.selectbox(
                    f"Attaque {j+1}",
                    available_moves,
                    index=0,
                    key=f"team1_move_{i}_{j}"
                )
                selected_moves.append(move)
            
            team1_pokemon.append({
                'name': pokemon_name,
                'level': level,
                'moves': selected_moves
            })

# ═══ ÉQUIPE 2 ═══
with col2:
    st.subheader("🔴 Équipe 2 (IA)")
    
    # Sélection du nombre de Pokémon
    nb_pokemon_2 = st.selectbox(
        "Nombre de Pokémon",
        [1, 2, 3, 4, 5, 6],
        index=0,
        key="nb_pokemon_2"
    )
    
    team2_pokemon = []
    for i in range(nb_pokemon_2):
        with st.expander(f"Pokémon {i+1}", expanded=(i == 0)):
            # Sélection du Pokémon
            pokemon_name = st.selectbox(
                f"Pokémon {i+1}",
                noms,
                index=noms.index("Bulbasaur") if "Bulbasaur" in noms and i == 0 else (i + 10) % len(noms),
                key=f"team2_pokemon_{i}"
            )
            
            # Niveau
            level = st.slider(
                f"Niveau",
                1, 100, 50,
                key=f"team2_level_{i}"
            )
            
            # Sélection des mouvements
            pokemon_row = pokemon_df[pokemon_df['Name'] == pokemon_name].iloc[0]
            pokemon_id = pokemon_row['Id']
            
            possible_move_ids = learn_df.loc[
                learn_df['pokemon_id'] == pokemon_id,
                'move_id'
            ].unique()
            
            possible_moves = (
                moves_df
                .loc[moves_df['id'].isin(possible_move_ids), 'name']
                .sort_values()
                .tolist()
            )
            
            selected_moves = []
            for j in range(4):
                available_moves = [mv for mv in possible_moves if mv not in selected_moves]
                if not available_moves:
                    available_moves = possible_moves
                
                move = st.selectbox(
                    f"Attaque {j+1}",
                    available_moves,
                    index=0,
                    key=f"team2_move_{i}_{j}"
                )
                selected_moves.append(move)
            
            team2_pokemon.append({
                'name': pokemon_name,
                'level': level,
                'moves': selected_moves
            })

# ─── Options de combat ────────────────────────────────────────────────────────

st.markdown("---")
st.header("⚙️ Options de Combat")

col1, col2, col3 = st.columns(3)

with col1:
    combat_mode = st.selectbox(
        "Mode de Combat",
        ["Automatique (IA vs IA)", "Manuel (Joueur vs IA)"],
        index=0
    )

with col2:
    max_turns = st.slider(
        "Nombre maximum de tours",
        10, 100, 50
    )

with col3:
    animation_speed = st.selectbox(
        "Vitesse d'animation",
        ["Lente (2s)", "Normale (1s)", "Rapide (0.5s)", "Instantané"],
        index=1
    )

# ─── Fonction de création des équipes ─────────────────────────────────────────

def create_team(team_data, team_name):
    """Crée une équipe de Pokémon à partir des données de configuration."""
    pokemon_list = []
    
    for pokemon_config in team_data:
        # Créer le Pokémon
        pokemon = factory.create_pokemon(pokemon_config['name'], pokemon_config['level'])
        
        # Ajouter les mouvements
        for move_name in pokemon_config['moves']:
            factory.add_move_to_pokemon(pokemon, move_name)
        
        pokemon_list.append(pokemon)
    
    return Team(pokemon_list, team_name)

# ─── Fonction de simulation de combat ─────────────────────────────────────────

def simulate_battle(team1, team2, max_turns, is_manual=False):
    """Simule un combat complet entre deux équipes."""
    
    battle_log = []
    turn_count = 0
    
    # Conteneurs pour l'affichage en temps réel
    status_container = st.container()
    battle_container = st.container()
    
    while not team1.is_defeated() and not team2.is_defeated() and turn_count < max_turns:
        turn_count += 1
        
        # Ajouter le marqueur de tour dans le journal
        battle_log.append(f"🎯 Tour {turn_count}")
        
        # Affichage du statut actuel
        with status_container:
            st.markdown(f"### 🎯 Tour {turn_count}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**🔵 {team1.name}**")
                st.markdown(f"Pokémon actif: **{team1.active_pokemon.name}** (Niv. {team1.active_pokemon.level})")
                current_hp = max(0, round(team1.active_pokemon.current_stats.health))
                max_hp = team1.active_pokemon.base_stats.health
                hp_percentage = (current_hp / max_hp) * 100 if max_hp > 0 else 0
                
                # Couleur de la barre selon les HP
                if hp_percentage > 50:
                    hp_color = "🟢"
                elif hp_percentage > 20:
                    hp_color = "🟡"
                else:
                    hp_color = "🔴"
                
                st.progress(hp_percentage / 100, text=f"{hp_color} {current_hp}/{max_hp} HP ({hp_percentage:.1f}%)")
                
                if current_hp == 0:
                    st.error("💀 KO!")
            
            with col2:
                st.markdown(f"**🔴 {team2.name}**")
                st.markdown(f"Pokémon actif: **{team2.active_pokemon.name}** (Niv. {team2.active_pokemon.level})")
                current_hp = max(0, round(team2.active_pokemon.current_stats.health))
                max_hp = team2.active_pokemon.base_stats.health
                hp_percentage = (current_hp / max_hp) * 100 if max_hp > 0 else 0
                
                # Couleur de la barre selon les HP
                if hp_percentage > 50:
                    hp_color = "🟢"
                elif hp_percentage > 20:
                    hp_color = "🟡"
                else:
                    hp_color = "🔴"
                
                st.progress(hp_percentage / 100, text=f"{hp_color} {current_hp}/{max_hp} HP ({hp_percentage:.1f}%)")
                
                if current_hp == 0:
                    st.error("💀 KO!")
        
        # Si les deux équipes ont encore des Pokémon valides
        if not team1.is_defeated() and not team2.is_defeated():
            
            # Déterminer l'ordre d'attaque basé sur la vitesse
            speed1 = team1.active_pokemon.current_stats.speed
            speed2 = team2.active_pokemon.current_stats.speed
            
            if speed1 >= speed2:
                first_team, second_team = team1, team2
                first_label, second_label = "🔵", "🔴"
            else:
                first_team, second_team = team2, team1
                first_label, second_label = "🔴", "🔵"
            
            # Premier attaquant
            if not first_team.active_pokemon.is_fainted():
                best_move = rmm.find_best_move(first_team.active_pokemon, second_team.active_pokemon)
                attack_result = pdc.resolve_interaction(
                    attacker=first_team.active_pokemon,
                    defender=second_team.active_pokemon,
                    move=best_move.move,
                    random_multiplier=True
                )
                
                with battle_container:
                    st.markdown(f"#### {first_label} {first_team.active_pokemon.name} attaque!")
                    display_streamlit_battle_summary(
                        first_team.active_pokemon,
                        second_team.active_pokemon,
                        best_move,
                        attack_result
                    )
                
                # Appliquer les dégâts avec gestion des HP jusqu'à 0
                if not attack_result.missed:
                    hp_avant = round(second_team.active_pokemon.current_stats.health)
                    # Calculer les dégâts réels (limités par les HP restants)
                    degats_reels = min(attack_result.effective_damage, hp_avant)
                    second_team.active_pokemon.take_damage(attack_result.effective_damage)
                    hp_apres = round(second_team.active_pokemon.current_stats.health)
                    
                    max_hp = second_team.active_pokemon.base_stats.health
                    battle_log.append(
                        f"💥 {first_team.active_pokemon.name} utilise {attack_result.move.name} "
                        f"et inflige {degats_reels} dégâts à {second_team.active_pokemon.name}! "
                        f"({hp_avant} → {hp_apres}/{max_hp} HP)"
                    )
                    
                    if second_team.active_pokemon.is_fainted():
                        battle_log.append(f"💀 {second_team.active_pokemon.name} est KO!")
                else:
                    battle_log.append(f"❌ {first_team.active_pokemon.name} rate son attaque avec {attack_result.move.name}!")
            
            # Deuxième attaquant (si toujours en vie)
            if not second_team.active_pokemon.is_fainted() and not first_team.active_pokemon.is_fainted():
                best_move = rmm.find_best_move(second_team.active_pokemon, first_team.active_pokemon)
                attack_result = pdc.resolve_interaction(
                    attacker=second_team.active_pokemon,
                    defender=first_team.active_pokemon,
                    move=best_move.move,
                    random_multiplier=True
                )
                
                with battle_container:
                    st.markdown(f"#### {second_label} {second_team.active_pokemon.name} attaque!")
                    display_streamlit_battle_summary(
                        second_team.active_pokemon,
                        first_team.active_pokemon,
                        best_move,
                        attack_result
                    )
                
                # Appliquer les dégâts avec gestion des HP jusqu'à 0
                if not attack_result.missed:
                    hp_avant = round(first_team.active_pokemon.current_stats.health)
                    # Calculer les dégâts réels (limités par les HP restants)
                    degats_reels = min(attack_result.effective_damage, hp_avant)
                    first_team.active_pokemon.take_damage(attack_result.effective_damage)
                    hp_apres = round(first_team.active_pokemon.current_stats.health)
                    
                    max_hp = first_team.active_pokemon.base_stats.health
                    battle_log.append(
                        f"💥 {second_team.active_pokemon.name} utilise {attack_result.move.name} "
                        f"et inflige {degats_reels} dégâts à {first_team.active_pokemon.name}! "
                        f"({hp_avant} → {hp_apres}/{max_hp} HP)"
                    )
                    
                    if first_team.active_pokemon.is_fainted():
                        battle_log.append(f"💀 {first_team.active_pokemon.name} est KO!")
                else:
                    battle_log.append(f"❌ {second_team.active_pokemon.name} rate son attaque avec {attack_result.move.name}!")
        
        # Vérifier si des Pokémon sont KO et doivent être remplacés APRÈS les attaques
        if team1.active_pokemon.is_fainted():
            available_switches = team1.get_available_switches()
            if available_switches:
                ancien_pokemon = team1.active_pokemon.name
                team1.switch_to(available_switches[0])
                battle_log.append(f"")
                battle_log.append(f"🔄 {team1.name} rappelle {ancien_pokemon} et envoie {team1.active_pokemon.name}!")
                battle_log.append(f"✨ {team1.active_pokemon.name} entre en combat avec {team1.active_pokemon.current_stats.health}/{team1.active_pokemon.base_stats.health} HP")
        
        if team2.active_pokemon.is_fainted():
            available_switches = team2.get_available_switches()
            if available_switches:
                ancien_pokemon = team2.active_pokemon.name
                team2.switch_to(available_switches[0])
                battle_log.append(f"")
                battle_log.append(f"🔄 {team2.name} rappelle {ancien_pokemon} et envoie {team2.active_pokemon.name}!")
                battle_log.append(f"✨ {team2.active_pokemon.name} entre en combat avec {team2.active_pokemon.current_stats.health}/{team2.active_pokemon.base_stats.health} HP")
        
        # Pause pour l'animation
        battle_log.append("")  # Ligne vide pour séparer les tours
        if animation_speed == "Lente (2s)":
            time.sleep(2)
        elif animation_speed == "Normale (1s)":
            time.sleep(1)
        elif animation_speed == "Rapide (0.5s)":
            time.sleep(0.5)
    
    # Déterminer le vainqueur
    if team1.is_defeated():
        winner = team2
        loser = team1
    elif team2.is_defeated():
        winner = team1
        loser = team2
    else:
        winner = None  # Match nul (limite de tours atteinte)
    
    return winner, loser, battle_log, turn_count

# ─── Bouton de lancement du combat ────────────────────────────────────────────

st.markdown("---")

if st.button("🚀 LANCER LE COMBAT!", type="primary", use_container_width=True):
    
    # Créer les équipes
    team1 = create_team(team1_pokemon, "Équipe 1")
    team2 = create_team(team2_pokemon, "Équipe 2")
    
    st.markdown("---")
    st.header("⚔️ Combat en Cours")
    
    # Affichage des équipes
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔵 Équipe 1")
        for i, pokemon in enumerate(team1.pokemons):
            status = "🟢 Actif" if i == team1.active_index else "⚪ En réserve"
            st.markdown(f"- **{pokemon.name}** (Niv. {pokemon.level}) - {status}")
    
    with col2:
        st.markdown("### 🔴 Équipe 2")
        for i, pokemon in enumerate(team2.pokemons):
            status = "🟢 Actif" if i == team2.active_index else "⚪ En réserve"
            st.markdown(f"- **{pokemon.name}** (Niv. {pokemon.level}) - {status}")
    
    st.markdown("---")
    
    # Lancer la simulation
    is_manual = combat_mode == "Manuel (Joueur vs IA)"
    winner, loser, battle_log, total_turns = simulate_battle(team1, team2, max_turns, is_manual)
    
    # Affichage des résultats
    st.markdown("---")
    st.header("🏆 Résultats du Combat")
    
    if winner:
        st.success(f"🎉 **{winner.name}** remporte le combat en {total_turns} tours!")
        st.balloons()
        
        # Statistiques détaillées
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Tours totaux", total_turns)
        
        with col2:
            remaining_pokemon = len([p for p in winner.pokemons if not p.is_fainted()])
            st.metric("Pokémon restants (vainqueur)", remaining_pokemon)
        
        with col3:
            total_hp_remaining = sum(
                max(0, round(p.current_stats.health)) 
                for p in winner.pokemons if not p.is_fainted()
            )
            st.metric("HP total restant", total_hp_remaining)
        
        # État détaillé des équipes
        st.markdown("### 📊 État Final des Équipes")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"#### 🔵 {team1.name}")
            for i, pokemon in enumerate(team1.pokemons):
                current_hp = max(0, round(pokemon.current_stats.health))
                max_hp = pokemon.base_stats.health
                hp_percentage = (current_hp / max_hp) * 100 if max_hp > 0 else 0
                
                if current_hp > 0:
                    status_icon = "✅" if not pokemon.is_fainted() else "⚪"
                    st.success(f"{status_icon} **{pokemon.name}** (Niv. {pokemon.level}): {current_hp}/{max_hp} HP ({hp_percentage:.1f}%)")
                else:
                    st.error(f"💀 **{pokemon.name}** (Niv. {pokemon.level}): KO (0/{max_hp} HP)")
        
        with col2:
            st.markdown(f"#### 🔴 {team2.name}")
            for i, pokemon in enumerate(team1.pokemons):
                current_hp = max(0, round(pokemon.current_stats.health))
                max_hp = pokemon.base_stats.health
                hp_percentage = (current_hp / max_hp) * 100 if max_hp > 0 else 0
                
                if current_hp > 0:
                    status_icon = "✅" if not pokemon.is_fainted() else "⚪"
                    st.success(f"{status_icon} **{pokemon.name}** (Niv. {pokemon.level}): {current_hp}/{max_hp} HP ({hp_percentage:.1f}%)")
                else:
                    st.error(f"💀 **{pokemon.name}** (Niv. {pokemon.level}): KO (0/{max_hp} HP)")
        
    else:
        st.warning(f"⏱️ Combat terminé par limite de temps ({max_turns} tours)")
        
        # Même affichage détaillé pour un match nul
        st.markdown("### 📊 État Final des Équipes (Match Nul)")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"#### 🔵 {team1.name}")
            for i, pokemon in enumerate(team1.pokemons):
                current_hp = max(0, round(pokemon.current_stats.health))
                max_hp = pokemon.base_stats.health
                hp_percentage = (current_hp / max_hp) * 100 if max_hp > 0 else 0
                
                if current_hp > 0:
                    status_icon = "✅" if not pokemon.is_fainted() else "⚪"
                    st.info(f"{status_icon} **{pokemon.name}** (Niv. {pokemon.level}): {current_hp}/{max_hp} HP ({hp_percentage:.1f}%)")
                else:
                    st.error(f"💀 **{pokemon.name}** (Niv. {pokemon.level}): KO (0/{max_hp} HP)")
        
        with col2:
            st.markdown(f"#### 🔴 {team2.name}")
            for i, pokemon in enumerate(team2.pokemons):
                current_hp = max(0, round(pokemon.current_stats.health))
                max_hp = pokemon.base_stats.health
                hp_percentage = (current_hp / max_hp) * 100 if max_hp > 0 else 0
                
                if current_hp > 0:
                    status_icon = "✅" if not pokemon.is_fainted() else "⚪"
                    st.info(f"{status_icon} **{pokemon.name}** (Niv. {pokemon.level}): {current_hp}/{max_hp} HP ({hp_percentage:.1f}%)")
                else:
                    st.error(f"💀 **{pokemon.name}** (Niv. {pokemon.level}): KO (0/{max_hp} HP)")
    
    # Journal de combat amélioré
    with st.expander("📜 Journal de Combat Détaillé", expanded=False):
        st.markdown("**Déroulé complet du combat avec tous les événements:**")
        st.markdown("---")
        
        current_turn = 0
        for i, log_entry in enumerate(battle_log):
            if log_entry == "":  # Ligne vide = séparateur
                st.markdown("")
            elif "Tour" in log_entry and log_entry.startswith("🎯"):
                current_turn += 1
                st.markdown(f"### {log_entry}")
                st.markdown("---")
            elif log_entry.startswith("🔄"):  # Changement de Pokémon
                st.info(f"**{log_entry}**")
            elif log_entry.startswith("✨"):  # Entrée en combat
                st.success(f"*{log_entry}*")
            elif log_entry.startswith("💥"):  # Attaque réussie
                st.warning(f"**{log_entry}**")
            elif log_entry.startswith("💀"):  # KO
                st.error(f"**{log_entry}**")
            elif log_entry.startswith("❌"):  # Attaque ratée
                st.info(f"*{log_entry}*")
            else:
                st.text(log_entry)
        
        st.markdown("---")
        st.markdown(f"**Combat terminé après {total_turns} tours**")

# ─── Informations sur les nouveautés ─────────────────────────────────────────

st.markdown("---")
st.header("✨ Nouveautés de cette Version")

with st.expander("🆕 Fonctionnalités Ajoutées", expanded=False):
    st.markdown("""
    ### 🎮 Simulation de Combat Complet
    - **Combat multi-tours** : Simulation complète jusqu'à KO d'une équipe
    - **Gestion d'équipes** : Support de 1 à 6 Pokémon par équipe
    - **Changements automatiques** : Remplacement automatique des Pokémon KO
    - **Ordre d'attaque** : Basé sur les statistiques de vitesse
    
    ### 🤖 Intelligence Artificielle
    - **IA avancée** : Utilise RightMoveMachine pour choisir les meilleurs coups
    - **Stratégie adaptative** : L'IA s'adapte selon l'état du combat
    - **Calculs de dégâts réalistes** : Formules Pokémon authentiques
    
    ### 🎨 Interface Utilisateur
    - **Affichage en temps réel** : Barres de HP et statuts mis à jour
    - **Animations configurables** : Vitesse d'animation ajustable
    - **Journal détaillé** : Historique complet du combat
    - **Métriques de performance** : Statistiques de fin de combat
    
    ### 🔧 Architecture Technique
    - **Utilisation complète du projet** : Intégration de tous les modules
    - **Gestion d'état avancée** : Suivi précis des HP et statuts
    - **Optimisations** : Cache des données pour de meilleures performances
    """)

with st.expander("📁 Fichiers du Projet Utilisés", expanded=False):
    st.markdown("""
    ### 📦 Modules Intégrés
    - **`create_pokemon.py`** : Création et gestion des Pokémon
    - **`team.py`** : Gestion des équipes et changements
    - **`damage.py`** : Calculs de dégâts et interactions
    - **`right_move_machine.py`** : IA pour sélection des coups
    - **`display.py`** : Affichage des résultats de combat
    - **`stats.py`** : Gestion des statistiques et modificateurs
    - **`moves.py`** : Définition et gestion des attaques
    - **`config.py`** : Configuration et chemins des données
    - **`utils.py`** : Utilitaires pour lecture des données
    
    ### 📊 Données Utilisées
    - **`pokemon.csv`** : Base de données des Pokémon
    - **`moves.csv`** : Base de données des attaques
    - **`chart.csv`** : Tableau d'efficacité des types
    - **`pokemonMovesCanLearn.csv`** : Associations Pokémon-Attaques
    - **`natures.csv`** : Natures et modificateurs
    """)

st.markdown("---")
st.markdown("*Simulateur créé avec ❤️ en utilisant l'architecture complète du projet PokémonML*")