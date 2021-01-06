"""
Add your buy rules here.
"""

# installed imports
import yfinance


def buy_rule_1(ticker):
    """
    First buy rule.

    :return: True if the 52 week trend is positive.
    """
    # if the 52 week trend is positive, buy!
    if ticker.info["52WeekChange"] > 0:
        print(
            f"52 week change of {ticker.info['52WeekChange']} is positive, suggest BUY!"
        )
        return True
    return False


def buy_rule_2(ticker):
    """
    Second buy rule.

    :return: True if the current price is lower than the market open price. False otherwise.
    """

    # if the price has declined since market open, buy!
    if ticker.info["regularMarketOpen"] - ticker.info["regularMarketPrice"] > 0:
        print(
            f"Current price of {ticker.info['regularMarketPrice']} is less than the opening price of {ticker.info['regularMarketOpen']}, suggest BUY"
        )
        return True
    return False


def is_buy(ticker: yfinance.Ticker):
    """
    Use this function to return True if the stock looks like a BUY, or False if it doesn't look like a BUY.

    :param ticker: the Ticker object containing information about a stock.
    :return: True if we should indicate a "buy" signal, False otherwise.
    """

    # implement your own, better rules (and check that the examples are what the comments say they are!)
    buy_rules = [buy_rule_1, buy_rule_2]
    for buy_rule in buy_rules:
        try:
            if buy_rule(ticker):
                print(f"Buy rule function {buy_rule} indicates a buy!")
                return True

        # some cases, such as when a ticker symbol is invalid, produce errors on indexing into 'ticker' objects.
        except ValueError as e:
            print(f"Problem examining the ticker: {e}")

            # don't issue a buy ruling when we had a problem
            return False
    return False

    # if we didn't hit any "buy trigger" rules, tell caller we're not interested in buying it.
    return False