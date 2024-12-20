import pandas as pd

def dbs_csv_to_df(csv_file_directory):
    df = pd.read_csv(csv_file_directory, skiprows=7)
    df["Transaction Date"] = pd.to_datetime(df["Transaction Date"])

    return df

def ocbc_csv_to_df(csv_file_directory):
    pass

if __name__ == "__main__":
    print(dbs_csv_to_df("./transaction_history_csv/November.csv"))
