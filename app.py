"""
Starter program for stock analysis.

Run this program by typing this in a terminal window:

python app.py --ticker msft
"""
# standard imports (included with python)
import argparse
import time
import threading

# installed imports (externa libraries)
import yfinance

# interval to wait between updates for ticker information.
UPDATE_INTERVAL_SEC = 10


def get_stock_info(ticker: str):
    """
    Get stock information for 'ticker'.

    :param ticker: the stock ticker, e.g. 'tsla'
    :return: dictionary (dict) of stock info, or None if no stock information was
    available.
    """

    # since we're not sure if the library supports mixed case ticker names, force the entire ticker to lowercase.
    ticker = ticker.lower()

    # any problem looking up stock information using the library will be handled with a generic failure.
    try:
        stock = yfinance.Ticker(ticker)
    except Exception as _:
        print(f"Error getting stock info for {ticker}")
        return None

    return stock


def check_fn(ticker: yfinance.Ticker):
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


def monitor_stock(ticker: str, should_buy_fn, event: threading.Event, interval: int):
    """
    Threaded function to monitor the status of a stock in a loop.

    :param ticker: the stock ticker to monitor.
    :param should_buy_fun: Function that tells us when to buy.
    :param event: signal the thread to exit.
    :param interval: the interval, in seconds, to wait between polls for fresh
    stock information.
    """

    # tell python we're referring to the global variable, and not a local one.
    while True:
        print(f"Checking on {ticker}")

        # call helper which uses special library to obtain stock information.
        stock = get_stock_info(ticker)
        if stock is None:
            print("Failed getting stock info, can't check if we should buy it...")
        else:
            # call user function to "analyze" stock
            if should_buy_fn(stock):
                print("BUY")
            else:
                print("DON'T BUY")

        # wait for either termination signal or interval, whichever is shorter.
        print(f"Waiting {UPDATE_INTERVAL_SEC} seconds...")
        if event.wait(interval):
            print("Thread signalled, exiting...")
            return


def main(args):
    """
    Called by the entry point.

    :param args: args
    :return: True if this function runs successfully. False otherwise.
    """

    print(f"Getting stock info for ticket {args.ticker}")

    # start a thread to call the check function over and over.
    event = threading.Event()
    thread = threading.Thread(
        target=monitor_stock,
        args=(args.ticker, check_fn, event, UPDATE_INTERVAL_SEC),
    )
    thread.start()

    # wait for user to press ctrl+c
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt as _:
        print("Exiting")
    finally:

        # tell python we're referring to the global variable, and not a local one.
        print("Waiting for thread to finish...")

        # tell the thread it can exit...
        event.set()

        # wait for the thread to finish cleanly.
        thread.join()
        print("Thread finished...")

    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # figure out which stock the user wants to get info for.
    parser.add_argument("--ticker", default="MSFT")

    args = parser.parse_args()

    assert main(args)