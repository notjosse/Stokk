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
    # exp_date = expiration_dates[0]

    fast_info = ticker_data[ticker].fast_info

    lastPrice = fast_info['lastPrice']
    dayChange = float(fast_info['lastPrice']) - float(fast_info['open'])

    # options = ticker_data[ticker].option_chain(exp_date)

    # df = options.calls
    # options_dict = df.to_dict()

    # final_data = []

    new_exp_dates = []
    # convert expiration dates from tuple --> list of strings
    for i in expiration_dates:
        new_exp_dates.append(str(i))

    datetime_exp_dates = []
    # convert expiration dates from strings --> list of datetime objects
    for i in new_exp_dates:
        datetime_exp_dates.append(datetime.datetime.strptime(i, '%Y-%m-%d'))

    # Desired Data List
    lst = ['strike', 'impliedVolatility', 'bid', 'ask', 'lastPrice', 'change', 'volume', 'openInterest', 'inTheMoney']

    # for i in range(len(options_dict['bid'].keys())):
    #     temp_list = []
    #     for category in lst:
    #         temp_list.append(options_dict[category][i])
    #     final_data.append(temp_list)

    # # Convert exp_date from string to datetime object
    # exp_date = datetime.datetime.strptime(exp_date, '%Y-%m-%d')

    # trying to get all options for all expiry dates:
    all_options = {}
    for date in expiration_dates:
        all_options[date] = ticker_data[ticker].option_chain(date).calls.to_dict()

    all_data = {}
    for key, value in all_options.items():
        strikes = []
        for i in range(len(value['bid'].keys())):
            temp_list = []
            for category in lst:
                temp_list.append(value[category][i])
            strikes.append(temp_list)
        all_data[key] = strikes

    return render_template('options.html', data=all_data, ticker=ticker, exp_dates=new_exp_dates, dt_exp_dates=datetime_exp_dates, lastPrice=lastPrice, dayChange=dayChange, num_exp_dates=len(new_exp_dates))