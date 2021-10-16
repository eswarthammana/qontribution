import numpy as np
from pandas_datareader import data as web
import datetime
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm
from efficient_frontier import GetData

class ValueAtRisk:

    def __init__(self, tickers=['AAPL', 'WMT', 'TSLA', 'GE', 'AMZN', 'DB'], amount=10000, confidence=0.95, num_days=10):
        self.tickers = tickers
        self.amount = amount
        self.c = confidence
        self.n = num_days
        self.stock_data = self.stock_data_list()

    def download_data(self, start, end):
        return web.get_data_yahoo(self.tickers, start=start, end=end)['Adj Close']

    def calculate_weights(self):
        model = GetData(self.tickers, self.amount)
        d = model.get_optimum()
        val = list()
        for ticker in self.tickers:
            val.append(d[ticker])
        return np.array(val)

    def value_at_risk_monte_carlo(self):
        # Generate Var-Cov matrix
        cov_matrix = self.stock_data.cov()
        # Calculate mean returns for each stock
        avg_rets = self.stock_data.mean()
        weights = self.calculate_weights()
        # Calculate mean returns for portfolio overall, using dot product to 
        # normalize individual means against investment weights
        port_mean = avg_rets.dot(weights)
        # Calculate portfolio standard deviation
        port_stdev = np.sqrt(weights.T.dot(cov_matrix).dot(weights))
        # Calculate mean of investment
        mean_investment = (1+port_mean) * self.amount
        # Calculate standard deviation of investmnet
        stdev_investment = port_stdev * self.amount
        # Using SciPy ppf method to generate values for the
        # inverse cumulative distribution function to a normal distribution
        # Plugging in the mean, standard deviation of our portfolio as calculated above
        cutoff = norm.ppf(1-self.c, mean_investment, stdev_investment)
        return self.amount - cutoff

    def stock_data_list(self):
        # historical data - define START and END dates
        start = datetime.datetime(2012, 1, 1)
        end = datetime.date.today()
        stock_data = self.download_data(start, end)
        stock_data_returns = stock_data.pct_change()
        return stock_data_returns

    def get_value_at_risk_monte_carlo(self):
        data_var = dict()
        var = self.value_at_risk_monte_carlo()
        for x in range(1, self.n+1):
            st = str(x) + " day VaR @ " + str(self.c*100) + "% confidence"
            data_var[st] = np.round(var * np.sqrt(x), 2)
        return data_var, self.n
