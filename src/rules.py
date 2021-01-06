"""
Add your buy rules here.
"""

# installed imports
import yfinance


def is_buy(ticker: yfinance.Ticker):
    """
    Use this function to return True if the stock looks like a BUY, or False if it doesn't look like a BUY.
    """

    # implement your own, better rules (and check that the examples are what the comments say they are!)

    # if the 52 week trend is positive, buy!
    if ticker.info["52WeekChange"] > 0:
        print(
            f"52 week change of {ticker.info['52WeekChange']} is positive, suggest BUY!"
        )
        return True

    # if the price has declined since market open, buy!
    if ticker.info["regularMarketOpen"] - ticker.info["regularMarketPrice"] > 0:
        print(
            f"Current price of {ticker.info['regularMarketPrice']} is less than the opening price of {ticker.info['regularMarketOpen']}, suggest BUY"
        )
        return True

    # if we didn't hit any "buy trigger" rules, tell caller we're not interested in buying it.
    return False