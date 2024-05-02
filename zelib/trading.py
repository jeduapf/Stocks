from lumibot.brokers import Alpaca
from lumibot.backtesting import YahooDataBacktesting
from lumibot.strategies import Strategy
from lumibot.traders import Trader
from datetime import datetime

def API():
	API_KEY = "PKDS3NC94TKVRWJ1NK0A"
	API_SECRET = "9JpNGHOIhMwWDKLHANz9H09UQ58MfxWUSLR9AIiy"
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
	start_date = datetime(2022,10,10)
	end_date = datetime(2024,4,10)

	strategy = Trader(name = "FirstBot", broker = broker, 
						parameters = {"symbol":"SPY"})

	strategy.backtest(
		YahooDataBacktesting,
		start_date,
		end_date,
		parameters ={}
		)