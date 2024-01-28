
import pandas as pd

def csv_to_dict(file_path):
    """
    Converts a CSV file from Laji.fi to a dictionary.
    Uses the 'id' column as keys and the remaining columns as values.
    """
    # Read the CSV file with the correct delimiter
    data = pd.read_csv(file_path, delimiter=';')

    # Convert to dictionary
    data_dict = data.set_index('id').T.to_dict()

    return data_dict
