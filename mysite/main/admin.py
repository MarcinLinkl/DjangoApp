from django.contrib import admin
from django.urls import path
from .models import *
from django.shortcuts import render
from django import forms
import pandas as pd
from django.conf import settings
from sqlalchemy import create_engine

# user = settings.DATABASES['default']['USER']
# password = settings.DATABASES['default']['PASSWORD']
# database_name = settings.DATABASES['default']['NAME']
class CsvImportForm(forms.Form):
    csv_upload = forms.FileField()

class CustomerAdmin(admin.ModelAdmin):

    def get_urls(self):
        urls=super().get_urls()
        new_urls=[path('upload-csv/', self.upload_csv),]
        return new_urls + urls

    def upload_csv(self, request):

        if request.method == "POST":
            engine = create_engine('sqlite:///db.sqlite3')
            csv_file = request.FILES["csv_upload"]
            df = pd.read_csv(csv_file, header = [0, 1],encoding="utf-8")
            n_df = pd.DataFrame(df["Attributes"]["Symbols"])
            n_df.rename(columns={"Symbols":"Date"}, inplace=True)
            i=0
            for columns in df.Close:
                new_df = pd.DataFrame(n_df)
                new_df["Symbol"]=columns
                new_df["Close"]=df["Close"][columns]
                new_df["High"]=df["High"][columns]
                new_df["Low"]=df["Low"][columns]
                new_df["Open"]=df["Open"][columns]
                new_df["Volume"]=df["Volume"][columns]
                if i==0:
                    pd.set_option('display.max_rows', 550000)
                    print(new_df[300:2000])
                i=+1
                new_df.reset_index(drop=True, inplace=True)
                new_df.to_sql(GPW._meta.db_table, if_exists='append', con=engine, index=False)


        form = CsvImportForm()
        data = {"form": form}
        return render(request, "admin/csv_upload.html", data)
admin.site.register(GPW_TICKERS, CustomerAdmin)
admin.site.register(GPW, CustomerAdmin)
admin.site.register(MAIN_INDICES, CustomerAdmin)
admin.site.register(MAIN_INDICES_TICKERS, CustomerAdmin)

# Register your models here.
