
import json
import time


import django_tables2 as tables
import yfinance as yf
from yahoo_fin import stock_info as si
from django.core.serializers import serialize
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.shortcuts import render
import finnhub
import plotly.graph_objects as go
import pandas as pd
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import Akcje_GPWSerializer
from .functions import plot_candlestick_chart, get_data
from .models import *
from .update_gpw import update_gpw_table
import pandas_datareader.data as web

finnhub_api_key = 'c80p6u2ad3ie5egtcce0'
alpha_vantage_api_key = 'YX9741BHQFXIYA0B'

class NameTable(tables.Table):
    name = tables.Column()

def HomeView(request):
    GPW_tickers = GPW_tickers.objects.values("name", "symbol_stooq")

    if request.method == 'POST':
        choose = request.POST.get('dropdown_index')
        ticker_stooq = GPW_tickers.values_list("symbol_stooq", flat=True).get(name=choose)

        year_start = request.POST.get('year_start')
        year_end = request.POST.get('year_end')

        stocks_query = GPW.objects.filter(symbol=ticker_stooq).filter(
            date__range=[f'{year_start}-01-01', f'{year_end}-12-31'
                         ]).values("date", "open", "high", "close", "low", "volume")
    else:
        ticker_stooq = "WIG20.PL"
        stocks_query = GPW.objects.filter(symbol=ticker_stooq).filter(
            date__range=["2021-12-05", "2022-01-07"]).values(
            "date", "open", "high", "close", "low", "volume")

    print(stocks_query)
    data = get_data(stocks_query)

    context = {
        "tikers_GPW": GPW_tickers,
        'candlestick': plot_candlestick_chart(data, ticker_stooq)
    }

    if request.GET.get("update_gpw_db"):
        tickers_GPW = GPW_tickers.objects.values_list("ticker", flat=True)
        update_gpw_table(tickers_GPW)

    return render(request, 'chartss.html', context)



@api_view()
def chart(request, id):
    def change_cl(stock_data):
        stock_data.rename(columns={"Open": 'open', "High": 'high', "Low": 'low', "Close": 'close'}, inplace=True)
        stock_data.index.rename('date', inplace=True)
        return stock_data
    interval="1d"
    period="5y"
    if request.method == "GET":
        interval=request.GET.get("interval")

    if interval=="1h":
        period="1mo"
    elif interval=="1wk":
        period="10y"
    stock_1 = yf.download(id, period=period,interval=interval).dropna()

    stock_1=change_cl(stock_1)

    stock=si.get_analysts_info(id)
    print(stock)

    table = NameTable(stock)

    context = {
        "table": table,
        "data": stock,
        'candlestick': plot_candlestick_chart(stock_1, id, F'{id} {interval} chart'),



    }
    return render(request, 'chart.html', context )


@api_view()
def charts(request, id):
    stocks_query = GPW.objects.filter(symbol=id).filter(
        date__range=["2022-01-01", "2022-01-07"]).values(
        "date", "open", "high", "close", "low")
    serializer = Akcje_GPWSerializer(stocks_query, many=True)
    a = json.dumps(serializer.data)
    context = {
        "data": a
    }
    return render(request, 'HomeChartsOne.html')


@api_view()
def home1(request):
    a_down = "bx bx-down-arrow-alt down"
    a_up = "bx bx-up-arrow-alt"
    r_dow = "bx-rotate-90"

    def check_arrow(data):
        if data >= 0:
            return a_up
        else:
            return a_down

    def check_rocket(data):
        if data >= 0:
            return ''
        else:
            return r_dow

    def p2f(df):
        for col in df:
            df[col] = df[col].str.rstrip("%").astype(float)
        return df

    # today = date.today()
    # yesterday = today + timedelta(days=1)
    # download yahoo finance data
    us_stocks_tk = ["^IXIC", "^GSPC", "^DJI", "DX-Y.NYB", '^TNX', '^IRX', '^TYX']
    us_1 = yf.download(us_stocks_tk, period="5d")
    print(us_1)
    us_ = yf.download(us_stocks_tk, period="5d")['Close'].dropna()
    print(us_)
    us_stocks = us_.iloc[-2:]
    # dropna get first value, round
    us_stocks_pct = us_stocks.pct_change().dropna().iloc[0] * 100
    us_stocks_pct = us_stocks_pct.round(2)
    us_stocks_diff = us_stocks.diff().dropna().iloc[0].round(2)
    us_stocks = us_stocks.iloc[1].round(2)

    SP500 = {"value": us_stocks["^GSPC"],
             "diff": us_stocks_diff["^GSPC"],
             "pct": us_stocks_pct["^GSPC"],
             "arrow": check_arrow(us_stocks_diff["^GSPC"]),
             "rocket": check_rocket(us_stocks_diff["^GSPC"])
             }
    Nasdaq = {"value": us_stocks["^IXIC"],
              "diff": us_stocks_diff["^IXIC"],
              "pct": us_stocks_pct["^IXIC"],
              "arrow": check_arrow(us_stocks_diff["^IXIC"]),
              "rocket": check_rocket(us_stocks_diff["^IXIC"])
              }
    DJI = {"value": us_stocks["^DJI"],
           "diff": us_stocks_diff["^DJI"],
           "pct": us_stocks_pct["^DJI"],
           "arrow": check_arrow(us_stocks_diff["^DJI"]),
           "rocket": check_rocket(us_stocks_diff["^DJI"])
           }
    DXY = {"value": us_stocks["DX-Y.NYB"],
           "diff": us_stocks_diff["DX-Y.NYB"],
           "pct": us_stocks_pct["DX-Y.NYB"],
           "arrow": check_arrow(us_stocks_diff["DX-Y.NYB"]),
           "rocket": check_rocket(us_stocks_diff["DX-Y.NYB"])
           }

    daydata = yf.download(["^IXIC", "^DJI", "^GSPC", "DX-Y.NYB"], period="1d", interval="15m")['Close']

    dj_daydata = daydata["^DJI"].dropna()
    sp_daydata = daydata["^GSPC"].dropna()
    dxy_daydata = daydata["DX-Y.NYB"].dropna()
    nq_daydata = daydata["^IXIC"].dropna()

    d_chart = {"dxy_labels": dxy_daydata.index.strftime("%H:%M:%S").tolist(),
               "dxy_data": dxy_daydata.values.round(2).tolist(),
               "sp_labels": sp_daydata.index.strftime("%H:%M:%S").tolist(),
               "sp_data": sp_daydata.values.round(2).tolist(),
               "dj_labels": dj_daydata.index.strftime("%H:%M:%S").tolist(),
               "dj_data": dj_daydata.values.round(2).tolist(),
               "nq_labels": nq_daydata.index.strftime("%H:%M:%S").tolist(),
               "nq_data": nq_daydata.values.round(2).tolist()
               }

    def day_most(typ='active', num=10):
        if typ == "active":
            data = si.get_day_most_active(num)
        elif typ == "gainers":
            data = si.get_day_gainers(num)
        elif typ == "losers":
            data = si.get_day_losers(num)
        data.fillna("-",inplace=True)
        print(data)
        data.to_dict()
        data["Price"] = data.pop("Price (Intraday)")
        data["Per_change"] = data.pop("% Change")
        data["Avg_vol_3m"] = data.pop("Avg Vol (3 month)").astype(int, errors='ignore')
        data["Market_cap"] = data.pop("Market Cap")
        data["Volume"] = data["Volume"].astype(int)
        data["Vol2avg"] = ((data["Volume"] / data["Avg_vol_3m"]) * 100).astype(int, errors='ignore')
        data["PE_ratio"] = data.pop("PE Ratio (TTM)")
        return data


    def get_futures(num=10):
        futures = si.get_futures().head(num)
        futures.to_dict()
        futures["Price"] = futures.pop("Last Price")
        futures["Per_change"] = futures.pop("% Change")
        return futures

    day_most_active = day_most()
    day_most_gainers = day_most("gainers")
    day_most_losers = day_most("losers")
    futures = get_futures()

    if request.method == "GET":
        if request.GET.get("active_see_all"):
            day_most_active = day_most(num=100)
        if request.GET.get("gainers_see_all"):
            day_most_gainers = day_most("gainers", num=100)
        if request.GET.get("losers_see_all"):
            day_most_losers = day_most("losers", num=100)
        if request.GET.get("futures_see_all"):
            futures = get_futures(num=100)

    us_sectors = web.get_sector_performance_av(api_key=alpha_vantage_api_key)
    us_sectors = p2f(us_sectors)


    us_se = {"labels": us_sectors.index.tolist(),
             "RT": us_sectors.iloc[:, 0].tolist(),
             "1D": us_sectors.iloc[:, 1].tolist(),
             "5D": us_sectors.iloc[:, 2].tolist(),
             "1M": us_sectors.iloc[:, 3].tolist(),
             "3M": us_sectors.iloc[:, 4].tolist(),
             "YTD": us_sectors.iloc[:, 5].tolist(),
             "1Y": us_sectors.iloc[:, 6].tolist(),
             "3Y": us_sectors.iloc[:, 7].tolist(),
             "5Y": us_sectors.iloc[:, 8].tolist(),
             }

    context = {
        "SP": SP500,
        "NQ": Nasdaq,
        "DJ": DJI,
        "DXY": DXY,
        "CHART": d_chart,
        "active": day_most_active,
        "gainers": day_most_gainers,
        "losers": day_most_losers,
        "SECTORS": us_se,
        "home": "active",
        "fu":futures,


    }

    return render(request, 'home.html', context)


# @api_view()
def finance_chart(request):
    # x,o,h,l,c=[]
    id = "AGT.PL"
    stocks_query = GPW.objects.filter(symbol=id).filter(
        date__range=["2022-01-01", "2022-01-07"]).values(
        "date", "open", "high", "close", "low").order_by("date")
    serializer = Akcje_GPWSerializer(stocks_query, many=True)
    # for entry in stocks_query:
    #     x.append(entry['date'])
    #     o.append(entry['open'])
    #     h.append(entry['high'])
    #     l.append(entry['low'])
    #     c.append(entry['close'])
    a = json.dumps(serializer.data)
    data = {"datasets": [{
        "data": a}]}
    return JsonResponse(data, safe=False)

def make_charts_df(tk,period="1d", interval="5m"):
    dx_df = yf.download(tk, period=period, interval=interval)

    print(dx_df)
    data = pd.DataFrame(dx_df, columns=['Open', "High", 'Low', 'Close']).round(2)
    df=[]
    for i, j in data.iterrows():
        dict_xohlc={
        "x":int(time.mktime(i.timetuple())*1000),
        "o":j["Open"],
        "h":j["High"],
        "l":j["Low"],
        "c":j["Close"],
        }
        df.append(dict_xohlc)
    return df


def make_charts_each_day(tk, period="10d", interval="1h"):
    dx_df = yf.download(tk, period=period, interval=interval)
    dx_df = pd.DataFrame(dx_df, columns=['Open', "High", 'Low', 'Close']).round(2)
    DFList = [group[1] for group in dx_df.groupby(dx_df.index.day)]
    print(DFList)
    df_full = []
    for items in DFList:
        df = []
        for i, j in items.iterrows():
            dict_xohlc = {
                "x": int(time.mktime(i.timetuple()) * 1000),
                "o": j["Open"],
                "h": j["High"],
                "l": j["Low"],
                "c": j["Close"],
            }
            df.append(dict_xohlc)
        df_full.append(df)
    return df_full


@api_view()
def WIG20(request):
    tk="WIG20.WA"
    datas = make_charts_each_day(tk,"20d","5m")

    print(datas)
    context = {"data": datas,
               "label":tk,
               "WIG20": "active"}
    return render(request, 'WIG20.html', context)

def home(request):
    a_down = "bx bx-down-arrow-alt down"
    a_up = "bx bx-up-arrow-alt"
    r_dow = "bx-rotate-90"

    def check_arrow(data):
        if data >= 0:
            return a_up
        else:
            return a_down

    def check_rocket(data):
        if data >= 0:
            return ''
        else:
            return r_dow

    def p2f(df):
        for col in df:
            df[col] = df[col].str.rstrip("%").astype(float)
        return df

    # today = date.today()
    # yesterday = today + timedelta(days=1)
    # download yahoo finance data
    us_stocks_tk = ["^IXIC", "^GSPC", "^DJI", "DX-Y.NYB", '^TNX', '^IRX', '^TYX']
    us_1 = yf.download(us_stocks_tk, period="5d")
    print(us_1)
    us_ = yf.download(us_stocks_tk, period="5d")['Close'].dropna()
    print(us_)
    us_stocks = us_.iloc[-2:]
    # dropna get first value, round
    us_stocks_pct = us_stocks.pct_change().dropna().iloc[0] * 100
    us_stocks_pct = us_stocks_pct.round(2)
    us_stocks_diff = us_stocks.diff().dropna().iloc[0].round(2)
    us_stocks = us_stocks.iloc[1].round(2)

    SP500 = {"value": us_stocks["^GSPC"],
             "diff": us_stocks_diff["^GSPC"],
             "pct": us_stocks_pct["^GSPC"],
             "arrow": check_arrow(us_stocks_diff["^GSPC"]),
             "rocket": check_rocket(us_stocks_diff["^GSPC"])
             }
    Nasdaq = {"value": us_stocks["^IXIC"],
              "diff": us_stocks_diff["^IXIC"],
              "pct": us_stocks_pct["^IXIC"],
              "arrow": check_arrow(us_stocks_diff["^IXIC"]),
              "rocket": check_rocket(us_stocks_diff["^IXIC"])
              }
    DJI = {"value": us_stocks["^DJI"],
           "diff": us_stocks_diff["^DJI"],
           "pct": us_stocks_pct["^DJI"],
           "arrow": check_arrow(us_stocks_diff["^DJI"]),
           "rocket": check_rocket(us_stocks_diff["^DJI"])
           }
    DXY = {"value": us_stocks["DX-Y.NYB"],
           "diff": us_stocks_diff["DX-Y.NYB"],
           "pct": us_stocks_pct["DX-Y.NYB"],
           "arrow": check_arrow(us_stocks_diff["DX-Y.NYB"]),
           "rocket": check_rocket(us_stocks_diff["DX-Y.NYB"])
           }

    daydata = yf.download(["^IXIC", "^DJI", "^GSPC", "DX-Y.NYB"], period="1d", interval="15m")['Close']

    dj_daydata = daydata["^DJI"].dropna()
    sp_daydata = daydata["^GSPC"].dropna()
    dxy_daydata = daydata["DX-Y.NYB"].dropna()
    nq_daydata = daydata["^IXIC"].dropna()

    d_chart = {"dxy_labels": dxy_daydata.index.strftime("%H:%M:%S").tolist(),
               "dxy_data": dxy_daydata.values.round(2).tolist(),
               "sp_labels": sp_daydata.index.strftime("%H:%M:%S").tolist(),
               "sp_data": sp_daydata.values.round(2).tolist(),
               "dj_labels": dj_daydata.index.strftime("%H:%M:%S").tolist(),
               "dj_data": dj_daydata.values.round(2).tolist(),
               "nq_labels": nq_daydata.index.strftime("%H:%M:%S").tolist(),
               "nq_data": nq_daydata.values.round(2).tolist()
               }

    def day_most(typ='active', num=10):
        if typ == "active":
            data = si.get_day_most_active(num)
        elif typ == "gainers":
            data = si.get_day_gainers(num)
        elif typ == "losers":
            data = si.get_day_losers(num)
        data.fillna("-",inplace=True)
        print(data)
        data.to_dict()
        data["Price"] = data.pop("Price (Intraday)")
        data["Per_change"] = data.pop("% Change")
        data["Avg_vol_3m"] = data.pop("Avg Vol (3 month)").astype(int, errors='ignore')
        data["Market_cap"] = data.pop("Market Cap")
        data["Volume"] = data["Volume"].astype(int)
        data["Vol2avg"] = ((data["Volume"] / data["Avg_vol_3m"]) * 100).astype(int, errors='ignore')
        data["PE_ratio"] = data.pop("PE Ratio (TTM)")
        return data


    def get_futures(num=10):
        futures = si.get_futures().head(num)
        futures.to_dict()
        futures["Price"] = futures.pop("Last Price")
        futures["Per_change"] = futures.pop("% Change")
        return futures

    day_most_active = day_most()
    day_most_gainers = day_most("gainers")
    day_most_losers = day_most("losers")
    futures = get_futures()

    if request.method == "GET":
        if request.GET.get("active_see_all"):
            day_most_active = day_most(num=100)
        if request.GET.get("gainers_see_all"):
            day_most_gainers = day_most("gainers", num=100)
        if request.GET.get("losers_see_all"):
            day_most_losers = day_most("losers", num=100)
        if request.GET.get("futures_see_all"):
            futures = get_futures(num=100)

    us_sectors = web.get_sector_performance_av(api_key=alpha_vantage_api_key)
    us_sectors = p2f(us_sectors)


    us_se = {"labels": us_sectors.index.tolist(),
             "RT": us_sectors.iloc[:, 0].tolist(),
             "1D": us_sectors.iloc[:, 1].tolist(),
             "5D": us_sectors.iloc[:, 2].tolist(),
             "1M": us_sectors.iloc[:, 3].tolist(),
             "3M": us_sectors.iloc[:, 4].tolist(),
             "YTD": us_sectors.iloc[:, 5].tolist(),
             "1Y": us_sectors.iloc[:, 6].tolist(),
             "3Y": us_sectors.iloc[:, 7].tolist(),
             "5Y": us_sectors.iloc[:, 8].tolist(),
             }
    datas=make_charts_df("^IXIC", "1d", "1h")

    context = {
        "SP": SP500,
        "NQ": Nasdaq,
        "DJ": DJI,
        "DXY": DXY,
        "data":datas,
        "CHART": d_chart,
        "active": day_most_active,
        "gainers": day_most_gainers,
        "losers": day_most_losers,
        "SECTORS": us_se,
        "home": "active",
        "fu":futures,


    }

    return render(request, 'home0.html', context)

