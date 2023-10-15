from flask import Blueprint, render_template
from flask_login import login_required
import pandas as pd
import yfinance as yf

options_data_bp = Blueprint("options_data", __name__, template_folder="templates")

# Options data route
@options_data_bp.route("/options")
@login_required
def options():

    tickers = ['AAPL', 'FB']
    ticker_data = {}

    for ticker in tickers:
        data = yf.Ticker(ticker)
        ticker_data[ticker] = data

    expiration_dates = ticker_data['AAPL'].options
    exp_date = expiration_dates[0]

    options = ticker_data['AAPL'].option_chain(exp_date)

    df = options.calls
    options_dict = df.to_dict()

    print(options_dict.keys())

    return options_dict

    # return render_template('options.html', data=options_dict)