from yahoo_fin import stock_info as si
import pandas as pd
import csv
import yfinance as yf
# a=si.tickers_dow()
# pd.DataFrame(a).to_csv('tickers_dow.csv', index=False)
# a=si.tickers_nasdaq()
# pd.DataFrame(a).to_csv('tickers_nasdaq.csv', index=False)
# a=si.tickers_other()
# pd.DataFrame(a).to_csv('tickers_other.csv', index=False)
# a=si.tickers_sp500()
# pd.DataFrame(a).to_csv('tickers_sp500.csv', index=False)
# print(si.tickers_other())
aapl_df = yf.download('AAIC-PC', 
                      start='2019-01-01', 
                      end='2021-06-12', 
                      progress=False,
)

print(aapl_df.head())
