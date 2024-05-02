import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
import datetime
import plotly.graph_objects as go

import time
import requests
import io

def get_stock (name = 'VALE', inicio = datetime.datetime(2003,2,11), fim = datetime.datetime(2022,2,11)):
    '''
    Input:
        name: Stock name as it is in the stock market of Yahoo
        inicio: Starting date
        fim: Ending date
    Output: 
        points: pd.dataframe type stock with columns (Open/High/Low/Close/Adj Close/Volume)
    '''
    assert isinstance(inicio,datetime.datetime) and isinstance(fim,datetime.datetime), "Variables inicio and fim must be datetime"

    try:
        # download the stock price
        stock = yf.download(name,start=inicio, end=fim, progress=False)
        
        # append the individual stock prices 
        if len(stock) == 0:
            ValueError("No data found")

    except Exception:
        ValueError('Failed downloading stock...')

    if isinstance(name,list):
        return stock
    else:
        return name,stock,len(stock)

def plot_stock(name, stock, feature = 'Close', fs = (14,9)):
    '''
    Input
        stock: pd.dataframe type stock with columns (Open/High/Low/Close/Adj Close/Volume)
        feature: Feature to extract
        fs: Figure size (horizontal, vertical)
    Output: 
        Plot the stock feature desired    
    '''
    # plt.figure(figsize = fs)
    # plt.plot(stock[feature])
    # plt.show()

    fig = go.Figure()
    if feature is not None:
        fig.add_trace(go.Scatter(x=stock.index, y=stock[feature], mode = 'lines', name=feature))
    else:
        fig.add_trace(go.Scatter(x=stock.index, y=stock['Open'], line=dict(color='royalblue', width=4), name='Open'))
        fig.add_trace(go.Scatter(x=stock.index, y=stock['Close'], line=dict(color='firebrick', width=4), name='Close'))
        fig.add_trace(go.Scatter(x=stock.index, y=stock['High'], line=dict(color='royalblue', width=4, dash='dot'), name='High'))
        fig.add_trace(go.Scatter(x=stock.index, y=stock['Low'], line=dict(color='firebrick', width=4, dash='dot'), name='Low'))

    fig.update_layout(title=f'Stock prices of {name}',
                   xaxis_title='Dates',
                   yaxis_title='Price')
    fig.show()

def get_points(stock, start = 0, step = 30, feature = 'Close'): 
    '''
    Input:
        stock: pd.dataframe type stock with columns (Open/High/Low/Close/Adj Close/Volume)
        start: Starting sampling points from data in days
        step: Amount of days between buying each piece of stock
        feature: Which feature of the stock to analyse from (Open/High/Low/Close/Adj Close/Volume)
    Output: 
        points: Equaly spaced pd.series type of list of the price of each chosen point
    '''

    return stock[feature][np.arange(start,len(stock),step,dtype = int)]

def get_brazil_tickers():
    br_tickers = pd.read_csv("./Reading/BR.csv")
    return list(br_tickers['Symbol'])

def test():
    inicio = datetime.datetime(2022,2,11)
    fim = datetime.datetime(2023,9,2)

    tickers = get_brazil_tickers()
    BR_Stocks = get_stock (tickers, inicio, fim)

    # Check if all stocks could be downloaded from the list
    if not len(set(tickers) - set(BR_Stocks['Close'].columns)) == 0:
        ValueError("There were stocks that couldn't be downloaded... Please remove or check them.")

    plot_stock("WEGE3.SA", "WEGE3.SA", feature = 'Close', fs = (14,9))

    # Swap by tickers name first in multicolumn index
    BR_Stocks = BR_Stocks.swaplevel(0, 1, 1)
    print(BR_Stocks.columns[0])

    # TODO: Clean NaNs by interpolating if sequence of NaNs are smaller than D days and if it's bigger, get data from the most recent 
    # date where the smallest NaN sequence is D days
    # https://stackoverflow.com/questions/29007830/identifying-consecutive-nans-with-pandas

    # TODO: For correlation matrix, is it necessary to take out NaNs? Maybe can just do the correlation first and it will only get the 
    # correct correlation between the exiwting days... Just set NaNs to zero? Must interpolate small NaN days first? 

