import pandas as pd
from django.core.management.base import BaseCommand
from sqlalchemy import create_engine

from main.models import *




class Command(BaseCommand):
    help = "A command to add data from an csv file to the datbase"
    def handle(self,*args, **options):

        file_csv = 'polskie gpw.csv'
        df = pd.read_csv(file_csv, header=None)
        df = df.iloc[:, 0:2]
        df.columns = ["ticker", "name"]
        engine= create_engine("sqlite:///db.sqlite3")
        df.to_sql(Akcje_GPW_tikery._meta.db_table,if_exists="append", con=engine, index=False,index_label=None)
