import random
import copy
from dataclasses import dataclass
from .data_loader import read_csv_data
from .create_pokemon import Pokemon


@dataclass
class Attack:
    damage_range: tuple  # (min_damage, max_damage)
    effective_damage: float  # Dégâts réellement infligés
    missed: bool  # True si l'attaque a raté
    crit: bool  # True si l'attaque a été un coup critique
    effectiveness: float  # Efficacité du move sur le Pokémon adverse
    defender: Pokemon  # Copie du Pokémon adverse tel qu'il était au moment de l'attaque
    attacker: Pokemon  # Copie du Pokémon attaquant tel qu'il était au moment de l'attaque


class PokemonDamageCalculator:
    """
    Classe pour calculer les dégâts d'une attaque en fonction des statistiques de combat et de l'efficacité des types.
    """

    def __init__(self, csv_path):
        """
        Charge le graphique d'efficacité des types à partir d'un fichier CSV.

        :param csv_path: Chemin vers le fichier CSV.
        """
        type_chart_df = read_csv_data(csv_path)
        type_chart_df.set_index('Attacking', inplace=True)
        self.type_chart = type_chart_df

    def get_effectiveness(self, attack_type, defender_type):
        """
        Récupère le multiplicateur d'efficacité pour un type d'attaque face au type du défenseur.

        :param attack_type: Type de l'attaque (ex: "Electric")
        :param defender_type: Type du défenseur (ex: "Water")
        :return: Multiplicateur sous forme de float (ex: 0.5, 1.0, 2.0)
        """
        return self.type_chart.loc[attack_type, defender_type]

    @staticmethod
    def get_random_damage_multiplier():
        """
        Retourne un multiplicateur de dégâts aléatoire (entre 0.85 et 1.00) selon une
        distribution non uniforme, comme dans les jeux officiels Pokémon.
        """
        weighted_values = (
                [85, 87, 89, 90, 92, 94, 96, 98] * 3 +  # 7.69% chacun
                [86, 88, 91, 93, 95, 97, 99] * 2 +  # 5.13% chacun
                [100]  # 2.56%
        )
        r = random.choice(weighted_values)
        print(f"Random damage multiplier (R): {r} → factor {r / 100:.2f}")
        return r / 100

    @staticmethod
    def is_crit_hit(pokemon):
        """
        Détermine si l'attaque est un coup critique en fonction de la chance critique du Pokémon.

        :param pokemon: Le Pokémon attaquant.
        :return: True si c'est un coup critique, False sinon.
        """
        return random.random() <= pokemon.base_stats.get_crit_chance()

    @staticmethod
    def move_hit(move):
        """
        Détermine si l'attaque touche en comparant une valeur aléatoire à la précision du move.
        """
        return random.uniform(0, 100) < move.accuracy

    def calculate_damage(self, attacker, defender, move):
        """
        Calcule les dégâts infligés par une attaque du Pokémon attaquant vers le défenseur.
        Retourne un objet Attack contenant toutes les informations calculées.

        :param attacker: Pokémon qui attaque.
        :param defender: Pokémon qui reçoit l'attaque.
        :param move: Objet move utilisé.
        :return: Objet Attack contenant la range de dégâts, les dégâts effectifs, si l'attaque a raté,
                 si c'est un coup critique, l'efficacité, ainsi que les copies des Pokémon impliqués.
        """
        # Vérifier si le move touche
        if not self.move_hit(move):
            print(f"{attacker.name}'s {move.name} missed!")
            return Attack(
                damage_range=(0, 0),
                effective_damage=0.0,
                missed=True,
                crit=False,
                effectiveness=0.0,
                defender=copy.deepcopy(defender),
                attacker=copy.deepcopy(attacker)
            )

        # Déterminer si c'est un coup critique et choisir les statistiques du défenseur en conséquence
        is_crit = self.is_crit_hit(attacker)
        defender_stats = defender.base_stats if is_crit else defender.current_stats
        if is_crit:
            print("It is a critical hit!")

        # Sélectionner les statistiques en fonction de la catégorie du move
        if move.damage_class == 'physical':
            attack_stat = attacker.current_stats.attack
            defense_stat = defender_stats.defense
        else:
            attack_stat = attacker.current_stats.attack_spe
            defense_stat = defender_stats.defense_spe

        # Formule de base pour le calcul des dégâts
        base_damage = (((2 * attacker.level / 5 + 2) * move.damage * (attack_stat / defense_stat)) / 50) + 2

        # Application du bonus STAB (Same-Type Attack Bonus)
        if move.element == attacker.type1 or move.element == attacker.type2:
            base_damage *= 1.5

        # Calcul de l'efficacité en fonction des types du défenseur
        effectiveness = self.get_effectiveness(move.element, defender.type1)
        if defender.type2:
            effectiveness *= self.get_effectiveness(move.element, defender.type2)
        print(f"Effectiveness of {move.element} against {defender.type1}/{defender.type2 or 'None'}: {effectiveness}")

        # Calcul de la range de dégâts (valeurs min et max)
        min_damage = round(base_damage * 0.85 * effectiveness, 2)
        max_damage = round(base_damage * effectiveness, 2)
        damage_range = (min_damage, max_damage)
        print(f"Damage Range {min_damage} - {max_damage}")

        # Facteur aléatoire
        random_factor = self.get_random_damage_multiplier()

        # Appliquer le multiplicateur de coup critique si nécessaire
        if is_crit:
            base_damage *= 1.5

        effective_damage = base_damage * effectiveness * random_factor

        # Retourner l'objet Attack avec copie des Pokémon pour éviter toute modification ultérieure
        return Attack(
            damage_range=damage_range,
            effective_damage=effective_damage,
            missed=False,
            crit=is_crit,
            effectiveness=effectiveness,
            defender=copy.deepcopy(defender),
            attacker=copy.deepcopy(attacker)
        )
