from flask import Flask, jsonify, request
from efficient_frontier import GetData
from value_at_risk import ValueAtRisk
from black_scholes import BlackScholes

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/portfolio', methods=['POST', 'GET'])
def optimal_portfolio():
    if request.method == 'POST':
        tickers = request.form['tickers']
        amount = request.form['amount']
        if len(tickers) > 0:
            da = [tic.replace(' ', '') for tic in tickers.split(',')]
            print(da, type(da))
            if len(amount) > 0:
                amount = int(amount)
                model = GetData(tickers=da, amount=amount)
            else:
                model = GetData(tickers=da)
        elif len(tickers) < 0 and len(amount) > 0:
            model = GetData(amount=amount)
        else:
            model = GetData()
        opt, amt = model.get_optimal_portfolio()
        return jsonify({'result' : opt}, {'amount' : amt})
    elif request.method == 'GET':
        pass

@app.route('/var', methods=['POST', 'GET'])
def value_at_risk():
    if request.method == 'POST':
        model = ValueAtRisk()
        data_var, n = model.get_value_at_risk_monte_carlo()
        return jsonify({'VaR' : data_var, 'number of days': n})

@app.route('/blackscholes', methods=['POST', 'GET'])
def black_scholes():
    if request.method == 'POST':
        S0 = float(request.form['initial'])
        E = float(request.form['expecetd'])
        T = float(request.form['time'])
        rf = float(request.form['riskfree'])
        sigma = float(request.form['sigma'])
        iterations = int(request.form['iterations'])
        model = BlackScholes(S0, E, T, rf, sigma, iterations)
        call, put = model.get_values()
        return jsonify({'BlackScholes' : {'call option': call, 'put option': put}})

if __name__ == '__main__':
    app.run()
