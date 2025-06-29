from .damage import Attack
from .create_pokemon import Pokemon
import streamlit as st


def display_turn_summary(attacker: Pokemon, defender: Pokemon, predicted_attack: Attack, executed_attack: Attack) -> None:
    """
    Print a detailed summary of a single battle turn, including:
    - The predicted best move.
    - The move that was actually executed.
    - Whether it hit or missed.
    - Damage dealt, critical hit status, and effectiveness.
    - HP state after the turn.

    Args:
        attacker (Pokemon): The Pokémon that performed the attack.
        defender (Pokemon): The Pokémon that was attacked.
        predicted_attack (Attack): The best move predicted before the turn.
        executed_attack (Attack): The actual move executed and its result.
    """
    print("\n" + "=" * 60)
    print("Pre-Turn Prediction")
    print("-" * 60)
    print(f"Expected best move: {predicted_attack.move.name} (PP: {predicted_attack.move.pp})")
    print(f"→ Estimated Damage: {predicted_attack.effective_damage:}")
    print(f"→ Effectiveness: x{predicted_attack.effectiveness:.2f}")
    print("=" * 60)

    print("Turn Execution")
    print("-" * 60)
    print(f"{attacker.name} uses {executed_attack.move.name} (PP left: {executed_attack.move.pp})")
    if executed_attack.missed:
        print("→ The move missed!")
    else:
        print(f"→ Deals {executed_attack.effective_damage:} damage to {defender.name}")
        if executed_attack.crit:
            print("→ It's a critical hit!")
        print(f"→ Effectiveness: x{executed_attack.effectiveness:.2f}")
    print("=" * 60)

    print("Post-Turn Status")
    print("-" * 60)
    print(f"{defender.name}'s HP: {round(defender.current_stats.health)} / {defender.base_stats.health}")
    print("=" * 60 + "\n")


def display_full_turn_summary(
    first_half: tuple,
    second_half: tuple | None
) -> None:
    sep = "=" * 60
    print("\n" + sep)
    print("Turn Prediction")
    print("-" * 60)

    # affiche first_half
    attacker, defender, move, result = first_half
    print(f"{attacker.name} use {move.name} (PP left: {move.pp})")
    if result.missed:
        print("The move missed")
    else:
        print(f"→ Deals {result.effective_damage} damage to {defender.name}")
        if result.crit:
            print("→ It's a critical hit!")
        print(f"→ Effectiveness: x{result.effectiveness:.2f}")

    print(sep)

    # affiche second_half si présent
    if second_half:
        attacker, defender, move, result = second_half
        print(f"{attacker.name} use {move.name} (PP left: {move.pp})")
        if result.missed:
            print("The move missed")
        else:
            print(f"→ Deals {result.effective_damage} damage to {defender.name}")
            if result.crit:
                print("→ It's a critical hit!")
            print(f"→ Effectiveness: x{result.effectiveness:.2f}")
        print(sep)
    else:
        print("Le défenseur est tombé KO avant de riposter.")
        print(sep)

    # post-turn status
    print("Post-Turn Status")
    print("-" * 60)
    # health mis à jour dans resolve_interaction
    for p in (first_half[1], second_half[1] if second_half else first_half[1]):
        print(f"{p.name}'s HP: {round(p.current_stats.health)} / {p.base_stats.health}")
        print("-" * 60)
    print()


def display_streamlit_battle_summary(attacker: Pokemon, defender: Pokemon, predicted_attack: Attack, executed_attack: Attack) -> None:
    """
    Affiche un résumé détaillé du tour de combat avec Streamlit, incluant :
    - Le meilleur coup prédit
    - Le coup réellement exécuté
    - Les dégâts, coups critiques et efficacité
    - L'état des HP après le tour
    
    Args:
        attacker (Pokemon): Le Pokémon qui attaque
        defender (Pokemon): Le Pokémon qui défend
        predicted_attack (Attack): Le meilleur coup prédit
        executed_attack (Attack): Le coup réellement exécuté
    """
    
    # Titre principal supprimé pour se concentrer sur les tours
    # st.markdown("### 🎯 Résumé du Combat")
    
    # Section Prédiction
    with st.container():
        st.markdown("#### 🔮 Prédiction Pré-Tour")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                label="Meilleur Coup Prédit",
                value=predicted_attack.move.name,
                help=f"PP restants: {predicted_attack.move.pp}"
            )
        
        with col2:
            st.metric(
                label="Dégâts Estimés",
                value=f"{predicted_attack.effective_damage}",
                help="Dégâts prédits avant exécution"
            )
        
        with col3:
            effectiveness_color = "normal"
            if predicted_attack.effectiveness > 1:
                effectiveness_color = "inverse"
            elif predicted_attack.effectiveness < 1:
                effectiveness_color = "off"
            
            st.metric(
                label="Efficacité",
                value=f"×{predicted_attack.effectiveness:.2f}",
                help="Multiplicateur d'efficacité du type"
            )
    
    st.divider()
    
    # Section Exécution
    with st.container():
        st.markdown("#### ⚔️ Exécution du Tour")
        
        # Informations sur l'attaque
        attack_info_col1, attack_info_col2 = st.columns(2)
        
        with attack_info_col1:
            st.markdown(f"**{attacker.name}** utilise **{executed_attack.move.name}**")
            st.caption(f"PP restants: {executed_attack.move.pp}")
        
        with attack_info_col2:
            if executed_attack.missed:
                st.error("💨 L'attaque a raté !")
            else:
                st.success("🎯 L'attaque a touché !")
        
        # Résultats de l'attaque si elle a touché
        if not executed_attack.missed:
            result_col1, result_col2, result_col3 = st.columns(3)
            
            with result_col1:
                damage_delta = executed_attack.effective_damage - predicted_attack.effective_damage
                st.metric(
                    label="Dégâts Réels",
                    value=f"{executed_attack.effective_damage}",
                    delta=f"{damage_delta:+}" if damage_delta != 0 else None,
                    help=f"Dégâts infligés à {defender.name}"
                )
            
            with result_col2:
                if executed_attack.crit:
                    st.metric(
                        label="Coup Critique",
                        value="✨ OUI",
                        help="L'attaque a fait un coup critique !"
                    )
                else:
                    st.metric(
                        label="Coup Critique",
                        value="❌ Non",
                        help="Pas de coup critique"
                    )
            
            with result_col3:
                effectiveness_emoji = "🟢" if executed_attack.effectiveness > 1 else "🔴" if executed_attack.effectiveness < 1 else "🟡"
                st.metric(
                    label="Efficacité réelle",
                    value=f"{effectiveness_emoji} ×{executed_attack.effectiveness:.2f}",
                    help="Multiplicateur d'efficacité final"
                )
    
    st.divider()
    
    # Section État Post-Combat
    with st.container():
        st.markdown("#### 💚 État Post-Combat")
        
        # Calcul du pourcentage de HP
        current_hp = round(defender.current_stats.health)
        max_hp = defender.base_stats.health
        hp_percentage = (current_hp / max_hp) * 100
        
        # Couleur de la barre de HP
        hp_color = "normal"
        if hp_percentage <= 25:
            hp_color = "off"
        elif hp_percentage <= 50:
            hp_color = "inverse"
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"**{defender.name}** - Points de Vie")
            st.progress(hp_percentage / 100, text=f"{current_hp} / {max_hp} HP ({hp_percentage:.1f}%)")
        
        with col2:
            hp_delta = -(executed_attack.effective_damage if not executed_attack.missed else 0)
            st.metric(
                label="HP Restants",
                value=f"{current_hp}",
                delta=f"{hp_delta}" if hp_delta != 0 else None,
                help=f"HP maximum: {max_hp}"
            )
    
    # Alerte si le Pokémon est KO
    if current_hp <= 0:
        st.error(f"💀 {defender.name} est K.O. !")
    elif hp_percentage <= 25:
        st.warning(f"⚠️ {defender.name} est en danger critique !")
    elif hp_percentage <= 50:
        st.info(f"🟡 {defender.name} est blessé.")
    
    st.markdown("---")
