from efficient_frontier import GetData

def optimal_portfolio(amount=None, tickers=[]):
    if len(tickers) > 0:
        da = [tic.replace(' ', '') for tic in tickers.split(',')]
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
    return ({'result' : opt}, {'amount' : amt})
