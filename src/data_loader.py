import pandas as pd

import pandas as pd


def read_csv_data(csv_path: str) -> pd.DataFrame:
    """
    Lit un fichier CSV et renvoie un DataFrame pandas.
    La fonction détecte automatiquement le séparateur, gère l'encodage et les valeurs manquantes.
    """
    try:
        # Essaye d'utiliser le séparateur standard ","
        data_frame = pd.read_csv(csv_path, encoding='utf-8')
    except UnicodeDecodeError:
        # Si problème d'encodage, réessaye avec latin1
        data_frame = pd.read_csv(csv_path, encoding='latin1')

    # Nettoyage des colonnes (enlève les espaces autour des noms)
    data_frame.columns = data_frame.columns.str.strip()

    return data_frame


def read_csv_data_Jules(csv_path: str) -> pd.DataFrame:
    """
    Read a csv file with pandas and return its data frame
    """
    data_frame = pd.read_csv(csv_path, sep=",")
    return data_frame
