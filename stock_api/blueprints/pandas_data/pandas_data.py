from flask import Blueprint
from flask_login import login_required

import datetime as dt
import pandas as pd
from pandas_datareader import data as pdr
import yfinance as yf
yf.pdr_override()


pandas_data_bp = Blueprint("pandas_data", __name__, template_folder="templates")

# Options data route
@pandas_data_bp.route("/pandas")
@login_required
def options():

    # set the start and end dates
    end_date = dt.datetime.now()
    start_date = dt.datetime(2010,1,1)

    # set the list of stocks to query
    stock_list = ['F', 'MSFT', 'AAPL', 'O']

    # structure/send the request and return a dataframe
    df = pdr.get_data_yahoo(stock_list, start=start_date, end=end_date)

    # convert the indexes from timestamps to strings
    df.index = df.index.map(str)

    # Return only the Close Data
    close = df.Close.head()

    # convert data to dictionary
    close_dict = close.to_dict()

    return [{"statistical_data": close.describe().to_dict()}, {"close_data":close_dict}]