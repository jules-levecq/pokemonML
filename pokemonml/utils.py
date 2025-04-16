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


def load_natures(csv_path: str) -> dict:
    """
    Load Pokémon natures from a CSV file and return them as a dictionary.

    Each nature defines stat modifiers that increase or decrease specific stats
    (e.g., Attack, Defense, Speed) during stat calculation. This function parses
    the nature definitions and returns a nested dictionary where each key is the
    name of a nature, and the corresponding value is a dictionary mapping each
    affected stat to its multiplier.

    The expected CSV structure should include the following columns:
        - "Nature"     : Name of the nature (e.g., "Adamant", "Modest", etc.)
        - "Attack"     : Multiplier for Attack (e.g., 1.1, 0.9, or 1.0)
        - "Defense"    : Multiplier for Defense
        - "Sp. Atk"    : Multiplier for Special Attack
        - "Sp. Def"    : Multiplier for Special Defense
        - "Speed"      : Multiplier for Speed

    Example return format:
    {
        "Adamant": {"Attack": 1.1, "Defense": 1.0, "Sp. Atk": 0.9, "Sp. Def": 1.0, "Speed": 1.0},
        ...
    }

    Args:
        csv_path (str): Path to the CSV file containing nature definitions.

    Returns:
        dict: A dictionary where keys are nature names and values are dictionaries of stat multipliers.
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
