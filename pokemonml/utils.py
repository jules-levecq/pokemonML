import pandas as pd


def read_csv_data(csv_path: str) -> pd.DataFrame:
    """
    Read and clean a CSV file into a pandas DataFrame.

    This function attempts to read the file using UTF-8 encoding, with a fallback
    to Latin-1 if Unicode errors are encountered. It also strips any extra whitespace
    from column names for easier downstream processing.

    Args:
        csv_path (str): The path to the CSV file to be read.

    Returns:
        pd.DataFrame: Cleaned DataFrame containing the CSV contents.
    """
    try:
        df = pd.read_csv(csv_path, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(csv_path, encoding='latin1')

    df.columns = df.columns.str.strip()  # Clean column names
    return df


def load_natures(csv_path):
    """
    Charge les natures depuis un fichier CSV et retourne un dictionnaire.

    Le dictionnaire aura pour clés les noms de nature et comme valeur un autre
    dictionnaire qui associe chaque stat à son multiplicateur.
    """
    df = pd.read_csv(csv_path)
    natures = {}
    for _, row in df.iterrows():
        nature_name = row["Nature"]
        natures[nature_name] = {
            "Attack": row["Attack"],
            "Defense": row["Defense"],
            "Sp. Atk": row["Sp. Atk"],
            "Sp. Def": row["Sp. Def"],
            "Speed": row["Speed"]
        }
    return natures
