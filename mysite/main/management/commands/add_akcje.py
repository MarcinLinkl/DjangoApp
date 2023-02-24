import pandas as pd
from django.core.management.base import BaseCommand
from sqlalchemy import create_engine
import csv
from main.models import *




class Command(BaseCommand):
    help = "A command to add data from an csv file to the datbase"
    def handle(self,*args, **options):

        file_csv = 'polish_stocks.csv'
        df = pd.read_csv(file_csv, header=[0, 1])
        pd.set_option('display.max_rows', 500)
        print(df[300:700])
        n_df = pd.DataFrame(df["Attributes"]["Symbols"])
        n_df.rename(columns={"Symbols": "Date"}, inplace=True)
        i = 0
        for columns in df.Close:
            new_df = pd.DataFrame(n_df)
            new_df["Symbol"] = columns
            new_df["Close"] = df["Close"][columns]
            new_df["High"] = df["High"][columns]
            new_df["Low"] = df["Low"][columns]
            new_df["Open"] = df["Open"][columns]
            new_df["Volume"] = df["Volume"][columns]
            if i == 0:
                pd.set_option('display.max_rows', 5500)
                print(new_df[300:700])
                i+=1
            else:
                break
