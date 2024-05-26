from lumibot.brokers import Alpaca
from lumibot.backtesting import YahooDataBacktesting
from lumibot.strategies import Strategy
from lumibot.traders import Trader
from datetime import datetime

import numpy as np
import pandas as pd
from zelib.plots import *
import os

def API():
    API_KEY = "PK0SE8ZHC11HHIVAWWHC"
    API_SECRET = "XiIkQr3jIhGWhhMFzTNpAwRfcWqR1XLzx3X7uP4X"
    BASE_URL = "https://paper-api.alpaca.markets/v2"

    ALPACA_CRED = {
        "API_KEY" : API_KEY,
        "API_SECRET" : API_SECRET,
        "PAPER" : True
    }
    return ALPACA_CRED


class Trader(Strategy):
    
    def initialize(self, symbol:str="SPY"):
        self.symbol = symbol
        self.sleeptime = '24H'
        self.last_trade = None

    def trading_iterations(self): 
        if self.last_trade is None:
            order = self.create_order(
                self.symbol,
                10,
                "buy",
                type = "market")
            self.submit_order(order)
            self.last_trade = "buy"

def test_trader():
    
    broker = Alpaca(API())
    start_date = datetime(2019,10,10)
    end_date = datetime(2021,4,10)

    strategy = Trader(name = "FirstBot", broker = broker, 
                        parameters = {"symbol":"SPY"})

    strategy.backtest(
        YahooDataBacktesting,
        start_date,
        end_date,
        parameters ={}
        )



class strategy_sma():

    def __init__(self, name, params):
        self.name = name
        self.profit = 0
        self.transactions = []
        self.M = 100
        self. params = params
        self.params['SMA'].sort()

        self.orders = {
                        "buy" : [],
                        "sell" : []
        }

    def __call__(self, data, feature = 'price_close', DELAY = True):

        df = data.copy()
        L = len(df)
        assert all([isinstance(p,int) and p < L/2 for p in self.params['SMA']]), "All SMA values must be integers lower than half of the amount of data points !"

        df['low_sma'] = df[feature].rolling(self.params['SMA'][0]).mean()
        df['high_sma'] = df[feature].rolling(self.params['SMA'][1]).mean()

        if DELAY:
            aux = np.where( (df['low_sma'] >= df['high_sma']) , True , False)
            df["buy"] = np.insert(aux & np.append(aux[1:], False) & ~np.insert(aux[:-1], 0, True, axis=0), 0, False, axis =0)[:-1]
            aux = np.where( (df['low_sma'] < df['high_sma']) , True , False)
            df["sell"] = np.insert(aux & np.append(aux[1:], False) & ~np.insert(aux[:-1], 0, True, axis=0), 0, False, axis =0)[:-1]
        else:
            aux = np.where( (df['low_sma'] >= df['high_sma']) , True , False)
            df["buy"] = aux & np.append(aux[1:], False) & ~np.insert(aux[:-1], 0, True, axis=0)
            aux = np.where( (df['low_sma'] < df['high_sma']) , True , False)
            df["sell"] = aux & np.append(aux[1:], False) & ~np.insert(aux[:-1], 0, True, axis=0)

        return df

    def backtest(self, data, feature = 'price_close', PLOT = False, DELAY = True, SAVE_DIR = './'):

        df = self.__call__(data, feature, DELAY)
        # L = list(df.max())[4:7]
        # m = np.min(L)
        # M = np.max(L)

        buy_orders_time = df['time_open'][df['buy']]
        buy_orders_price = np.array(df[feature][df['buy']])
        sell_orders_time = df['time_open'][df['sell']]
        sell_orders_price = np.array(df[feature][df['sell']])


        # TODO: organize buy and selling vectors ...
        b = len(buy_orders_time)
        s = len(sell_orders_time)
        if b < s:
            diff = s-b
            sell_orders_time = sell_orders_time[diff:]
            sell_orders_price = sell_orders_price[diff:]
        elif b > s:
            diff = b-s
            buy_orders_time = buy_orders_time[diff:]
            buy_orders_price = buy_orders_price[diff:]

        if all([ b < s for b,s in zip(buy_orders_time,sell_orders_time)]):
            self.profit =  100*( np.prod(np.divide(sell_orders_price, buy_orders_price)) - 1 )
            self.transactions = [100*(s/b-1) for b,s in zip(buy_orders_price,sell_orders_price)]

        if PLOT:
            fig = candlestick_plot(data)
            for s in self.params['SMA']:
                fig = add_SMA(  fig, data, 
                                color = f'rgba(0, {1275/s}, 255, 1)', 
                                feature = feature, SMA = s)

            anot = []
            shap = []
            for b,s,t in zip(buy_orders_time, sell_orders_time,self.transactions):
                shap.append(dict(
                                    x0=b, x1=b, y0=0, y1=1, xref='x', yref='paper',
                                    line_width=1,line_color="green"))
                shap.append(dict(
                                    x0=s, x1=s, y0=0, y1=1, xref='x', yref='paper',
                                    line_width=1,line_color="red"))
                anot.append(dict(
                                    x=b, y=0.8, xref='x', yref='paper',
                                    showarrow=False, xanchor='left', text='Buy'))
                anot.append(dict(
                                    x=s, y=0.8, xref='x', yref='paper',
                                    showarrow=False, xanchor='left', text=f'Sell<br>(Profit: {t:.2f}%)'))

            fig.update_layout(
                                title=f'Simple Moving Average (Profit: {self.profit:.3f}%)',
                                yaxis_title=feature,
                                shapes = shap,
                                annotations=anot
                            )

            fig.write_html(f"{os.path.join(SAVE_DIR,self.name)}.html")




