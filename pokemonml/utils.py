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
