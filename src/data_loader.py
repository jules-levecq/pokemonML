import pandas as pd
def read_csv_data(csv_path: str) -> pd.DataFrame:
    """
    Read a csv file with pandas and return its data frame
    """
    data_frame = pd.read_csv(csv_path, sep=",")
    return data_frame