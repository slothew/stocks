# Setup

Check out the code into a folder of your choosing, then in a terminal window:

```bash
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
```

# Run

```bash
python app.py --ticker tsla
```

Then press `Ctrl+C` to stop the program.

# Help

The library used to obtain stock information is hosted at https://github.com/ranaroussi/yfinance. See the README on that page for usage examples.
