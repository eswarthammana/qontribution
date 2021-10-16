import numpy as np

class BlackScholes:

    def __init__(self, S0=100, E=100, T=1, rf=0.05, sigma=0.2, iterations=10000):
        self.S0 = S0
        self.E = E
        self.T = T
        self.rf = rf
        self.sigma = sigma
        self.iterations = iterations

    def call_option_simulation(self):
        # we have 2 columns: first with 0s and second column will store the payoff
        # we need the first column of 0s: payoff function is max(0, S-E) for call option
        option_data = np.zeros([self.iterations, 2])
        
        # weiner process
        # dimensions: 1 dimensional array with as many items as the iterations
        # N(0,1)
        rand = np.random.normal(0, 1, [1, self.iterations])
        
        # equation for the s(t) stock price at T
        stock_price = self.S0 * np.exp((self.rf - 0.5 * self.sigma ** 2) * self.T + self.sigma * np.sqrt(self.T) * rand)
        
        # we need S-E because we have to calculate the max(S-E,0)
        option_data[:, 1] = stock_price - self.E
        
        # average for the monte-carlo simulation
        # max() returns the max(0, S-E) according to the formula
        average = np.sum(np.amax(option_data, axis=1)) / float(self.iterations)
        
        # we have to use the exp(-rt) discount factor
        return average * np.exp(-1.0 * self.rf * self.T) 

    def put_option_simulation(self):
        # we have 2 columns: first with 0s and second column will store the payoff
        # we need the first column of 0s: payoff function is max(0, E-S) for call option
        option_data = np.zeros([self.iterations, 2])
        
        # weiner process
        # dimensions: 1 dimensional array with as many items as the iterations
        # N(0,1)
        rand = np.random.normal(0, 1, [1, self.iterations])
        
        # equation for the s(t) stock price at T
        stock_price = self.S0 * np.exp((self.rf - 0.5 * self.sigma ** 2) * self.T + self.sigma * np.sqrt(self.T) * rand)
        
        # we need E-S because we have to calculate the max(E-S,0)
        option_data[:, 1] = self.E - stock_price
        
        # average for the monte-carlo simulation
        # max() returns the max(0, E-S) according to the formula
        average = np.sum(np.amax(option_data, axis=1)) / float(self.iterations)
        
        # we have to use the exp(-rt) discount factor
        return average * np.exp(-1.0 * self.rf * self.T)

    def print_values(self):
        print("Value of the call option is %.2f" %self.call_option_simulation())
        print("Value of the put option is %.2f" %self.put_option_simulation())

    def get_values(self):
        return self.call_option_simulation(), self.put_option_simulation() 
