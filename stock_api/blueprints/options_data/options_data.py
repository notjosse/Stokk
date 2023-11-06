from flask import Blueprint, render_template
from flask_login import login_required
import pandas as pd
import yfinance as yf
import datetime

options_data_bp = Blueprint("options_data", __name__, template_folder="templates")

# Options data route
@login_required
@options_data_bp.route("/options")
@options_data_bp.route("/options/<ticker>")
def options(ticker='AAPL'):

    ticker = ticker.upper()

    tickers = [ticker]
    ticker_data = {}

    for i in tickers:
        data = yf.Ticker(i)
        ticker_data[i] = data

    expiration_dates = ticker_data[ticker].options
    exp_date = expiration_dates[0]

    options = ticker_data[ticker].option_chain(exp_date)

    df = options.calls
    options_dict = df.to_dict()

    final_data = []

    print(options_dict.keys())

    # Desired Data List
    lst = ['strike', 'impliedVolatility', 'bid', 'ask', 'lastPrice', 'change', 'volume', 'openInterest', 'inTheMoney']

    for i in range(len(options_dict['bid'].keys())):
        temp_list = []
        for category in lst:
            temp_list.append(options_dict[category][i])
        final_data.append(temp_list)

    # Convert exp_date from string to datetime object
    exp_date = datetime.datetime.strptime(exp_date, '%Y-%m-%d')

    return render_template('options.html', data=final_data, ticker=ticker, exp_date=exp_date)