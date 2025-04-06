import pandas as pd


def read_csv_data(csv_path: str) -> pd.DataFrame:
    """
    Read a CSV file into a pandas DataFrame.

    This function attempts to automatically handle encoding issues and trims column names.

    :param csv_path: Path to the CSV file
    :return: A pandas DataFrame containing the file's contents
    """
    try:
        # Try using standard UTF-8 encoding
        data_frame = pd.read_csv(csv_path, encoding='utf-8')
    except UnicodeDecodeError:
        # Fallback to Latin-1 encoding in case of error
        data_frame = pd.read_csv(csv_path, encoding='latin1')

    # Strip whitespace from column names
    data_frame.columns = data_frame.columns.str.strip()

    return data_frame
