import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pandas_datareader as web
import yfinance as yf
import scipy.optimize as optimization

class GetData:
    def __init__(self, tickers=['AAPL', 'WMT', 'TSLA', 'GE', 'AMZN', 'DB'], amount=10000):
        self.tickers = tickers
        self.amount = amount
        self.daily_log_return, portfolio_weights = self.get_data()
        self.optimum = self.portfolio_optimize(portfolio_weights)
        self.print_optimal_portfolio()

    def get_data(self):
        stocks = {}
        for ticker in self.tickers:
            prices = web.DataReader(ticker, start='2018-06-20', end = '2021-06-20', data_source='yahoo')
            stocks[ticker] = prices['Adj Close']
        df_stocks = pd.DataFrame(stocks)
        daily_log_return = np.log(df_stocks/df_stocks.shift(1))[1:]
        NUM_PORTFOLIOS = 10000
        # generate portfolio's
        portfolio_means = []
        portfolio_risks = []
        portfolio_weights = []

        for _ in range(NUM_PORTFOLIOS):
            w = np.random.random(len(self.tickers))
            w /= np.sum(w) #Normalize for total sum equal to 1
            portfolio_weights.append(w)
        portfolio_weights = np.array(portfolio_weights)
        return daily_log_return, portfolio_weights

    def statistics(self, weights, returns):
        portfolio_return = np.sum(returns.mean() * weights) * 252
        portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(returns.cov() * 252, weights)))
        sharpe_ratio = portfolio_return / portfolio_volatility #risk free security is zero
        return np.array([portfolio_return, portfolio_volatility, sharpe_ratio])

    def min_function_shapre(self, weights, returns):
        return -self.statistics(weights, returns)[2]

    def portfolio_optimize(self, weights):
        constraints = {'type':'eq', 'fun':lambda x: np.sum(x) - 1}
        bounds = tuple((0, 1) for _ in range(len(self.tickers)))
        return optimization.minimize(fun=self.min_function_shapre, x0=weights[0], args=self.daily_log_return, method='SLSQP', bounds=bounds, constraints=constraints)

    def print_optimal_portfolio(self):
        print("Optimal portfolio: ", self.optimum['x'].round(3))
        print("Expected return, volatility and Sharpe ratio: ", self.statistics(self.optimum['x'].round(3), self.daily_log_return))

    def get_optimal_portfolio(self):
        data_dict = dict()
        amount_dict = dict()
        for ticker, value in zip(self.tickers, self.optimum['x']):
            try:
                pg = yf.Ticker(ticker)
                data_dict[pg.info['shortName']] = value
                amount_dict[pg.info['shortName']] = self.amount * value
            except:
                data_dict[ticker] = value
                amount_dict[ticker] = self.amount * value
        return data_dict, amount_dict

    def get_optimum(self):
        data_dict = dict()
        for ticker, value in zip(self.tickers, self.optimum['x']):
            data_dict[ticker] = value
        return data_dict

    def get_expected_values(self):
        return self.statistics(self.optimum['x'].round(3), self.daily_log_return)  
