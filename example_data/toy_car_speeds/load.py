import pandas as pd  # To install pandas, `pip install pandas`


def load_data(path):
    speeds = pd.DataFrame.from_csv(path).Y
    return list(zip(speeds.index, speeds))
