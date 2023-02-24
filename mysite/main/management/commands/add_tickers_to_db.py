import pandas as pd



def add_csv_to_db_tickers(file,table):
    df = pd.read_csv(file, header=None)
    print(df)