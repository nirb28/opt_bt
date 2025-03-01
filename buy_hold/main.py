from QuantConnect import *
from QuantConnect.Algorithm import *
from QuantConnect.Data import *

class BuyAndHoldStrategy(QCAlgorithm):
    def Initialize(self):
        # Set the cash we'd like to use for trading
        self.SetCash(100000)
        
        # Set the start date and end date for backtesting
        self.SetStartDate(2020, 1, 1)
        self.SetEndDate(2024, 12, 31)
        
        # Add equity that we want to trade (for example, SPY ETF)
        self.symbol = self.AddEquity("SPY", Resolution.Daily).Symbol
        
        # Set the brokerage model
        self.SetBrokerageModel(BrokerageName.InteractiveBrokersBrokerage)

    def OnData(self, data):
        # If we don't have any positions, enter position
        if not self.Portfolio.Invested:
            # Calculate the number of shares we can buy
            price = data[self.symbol].Close
            shares = self.Portfolio.Cash // price
            
            # Place the buy order
            self.MarketOrder(self.symbol, shares)
            self.Log(f"Buying {shares} shares of {self.symbol} at {price}")
