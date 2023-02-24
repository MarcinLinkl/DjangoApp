import pandas as pd
import pandas_datareader.data as web
import datetime as dt
import os

from sqlalchemy import create_engine

from .models import GPW


def update_gpw_table(tickers_GPW):
    list_tk = []
    for tk in tickers_GPW:
        list_tk.append(tk + ".PL")
    downloadData_from_to(list_tk,2021,1,1)


def downloadData_from_to(ticker, year, month, day):
    start_time = dt.datetime(year, month, day)
    end_time = dt.datetime.now().date().isoformat()  # today
    print("Day start collecting at {}.\nToday is {} ".format(start_time, end_time))
    print("Collecting {}...".format(ticker))
    df = web.DataReader(ticker, 'stooq', start_time, end_time)
    print(df)
    df = df.iloc[::-1]  # odwrócenie dat
    input1 = (input("save? [y/n]... \n enter:"))
    if input1 == 'y':
        input2 = (input("Enter file name: "))
        saveTo(df, input2)
    else:
        pass
    save_to(df)
    saveTo(df, 'polskie_akcje_GPW')


def save_to(df):
    df.columns = [df.iloc[0].values, df.iloc[1].values]
    df = df.iloc[2:].reset_index(drop=True)
    print(df.columns.values)
    n_df = pd.DataFrame(df["Attributes"]["Symbols"])

    n_df.rename(columns={"Symbols": "Date"}, inplace=True)
    engine = create_engine('sqlite:///db.sqlite3')

    for indexies in df.Close:
        new_df = pd.DataFrame(n_df)
        new_df["Symbol"] = indexies
        new_df["Close"] = df["Close"][indexies]
        new_df["High"] = df["High"][indexies]
        new_df["Low"] = df["Low"][indexies]
        new_df["Open"] = df["Open"][indexies]
        new_df["Volume"] = df["Volume"][indexies]
        new_df.reset_index(drop=True, inplace=True)
        print(new_df)
        new_df.to_sql(GPW._meta.db_table, if_exists='append', con=engine, index=False)



def saveTo(df, tickers):
    outdir = './stockdata/'
    if not os.path.exists(outdir):
        os.mkdir(outdir)

    outname = f"{tickers}.csv"
    fullname = os.path.join(outdir, outname)
    df.to_csv(fullname)
