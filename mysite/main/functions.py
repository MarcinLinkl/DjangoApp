import pandas as pd
import plotly.graph_objects as go
from plotly.offline import plot


def plot_candlestick_chart(df, ticker,title, df2=None, ticker2=None):
    df['MA12'] = df['close'].rolling(12).mean()
    df['MA50'] = df['close'].rolling(50).mean()
    df['MA100'] = df['close'].rolling(100).mean()
    df['MA200'] = df['close'].rolling(200).mean()
    ma12_scatter = go.Scatter(x=df.index.get_level_values('date'),
                              y=df['MA12'],
                              line=dict(color='green', width=0.2),
                              mode='lines', name='ma12')
    ma50_scatter = go.Scatter(x=df.index.get_level_values('date'),
                              y=df['MA50'],
                              line=dict(color='grey', width=0.4),
                              mode='lines', name='ma50')
    ma100_scatter = go.Scatter(x=df.index.get_level_values('date'),
                               y=df['MA100'],
                               line=dict(color='blue', width=0.6),
                               mode='lines', name='ma100')
    ma200_scatter = go.Scatter(x=df.index.get_level_values('date'),
                               y=df['MA200'],
                               line=dict(color='red', width=0.8),
                               mode='lines', name='ma200')
    candlestick1 = go.Candlestick(x=df.index.get_level_values('date'),
                                  open=df['open'],
                                  high=df['high'],
                                  low=df['low'],
                                  close=df['close'], name=ticker)

    fig = go.Figure(data=[candlestick1, ma12_scatter, ma50_scatter, ma100_scatter, ma200_scatter])
    fig.update_layout(title=title,title_x=0.5, title_font=dict(size=20))

    candlestick_div = plot(fig, output_type='div')
    return candlestick_div


def get_data(stocks_query):
    date = pd.DatetimeIndex(stocks_query.values_list("date", flat=True))
    open = pd.to_numeric(stocks_query.values_list("open", flat=True))
    data = pd.DataFrame(open, index=date, columns=['open'])
    data["high"] = pd.to_numeric(stocks_query.values_list("high", flat=True))
    data["close"] = pd.to_numeric(stocks_query.values_list("close", flat=True))
    data["low"] = pd.to_numeric(stocks_query.values_list("low", flat=True))
    data["volume"] = pd.to_numeric(stocks_query.values_list("volume", flat=True))
    data.dropna(inplace=True)
    data.index.name = "date"
    return data
