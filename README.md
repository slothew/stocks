# Stocks

Application to periodically check on stock information using the Yahoo Finance library from https://github.com/ranaroussi/yfinance.

## Prereqs

Tested on MacOS.

- Homebrew

  `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`

- git

  `brew install git`

- python 3.6 or higher

  `brew install python3`

- pypy 3.6 or higher

  `brew install pypy`

- virtualenv

  `pip install virtualenv`

## Install

Check out the code into a folder of your choosing, then in a terminal window:

```bash
mkdir -p ~/git
cd ~/git
git clone https://github.com/slothew/stocks.git
cd stocks
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
# poll for updates on the stock every 20 seconds
python -m src.app tsla --interval 20

# default polling interval
python -m src.app tsla

```

Then press `Ctrl+C` to stop the program.
