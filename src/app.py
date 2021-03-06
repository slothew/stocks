"""
Starter program for stock analysis.

Run this program by typing this in a terminal window:

python app.py tsla 

Or, specifying an interval:

python app.py msft --interval 20
"""
# standard imports (included with python)
import argparse
import time
import threading

# custom imports
from src import rules

# installed imports (externa libraries)
import yfinance

# minimum interval to wait between updates for ticker information.
MIN_UPDATE_INTERVAL_SEC = 10


def get_stock_info(ticker: str):
    """
    Get stock information for 'ticker'.

    :param ticker: the stock ticker, e.g. 'tsla'
    :return: Ticker object from the yfinance library.
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
            print(stock.info)
            if should_buy_fn(stock):
                print("BUY")
            else:
                print("DON'T BUY")

        # wait for either termination signal or interval, whichever is shorter.
        print(f"Waiting {interval} seconds...")
        if event.wait(interval):
            print("Thread signalled, exiting...")
            return


def main(args):
    """
    Called by the entry point.

    :param args: args
    :return: True if this function runs successfully. False otherwise.
    """

    # try and cap (albeit arbitrarily) the rate at which we hammer the yfinance data source...
    if args.interval < MIN_UPDATE_INTERVAL_SEC:
        print("Don't spam the yfinance API...")
        return False

    print(f"Getting stock info for ticket {args.ticker}")

    # start a thread to call the check function over and over.
    event = threading.Event()
    thread = threading.Thread(
        target=monitor_stock,
        args=(args.ticker, rules.is_buy, event, args.interval),
    )
    thread.start()

    # wait for user to press ctrl+c
    print("Press CTRL+C to exit.")
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
    parser.add_argument("ticker", help="Stock ticker symbol (e.g. 'tsla')")
    parser.add_argument(
        "--interval",
        help="delay between stock updates",
        type=int,
        default=MIN_UPDATE_INTERVAL_SEC,
    )

    args = parser.parse_args()

    assert main(args)