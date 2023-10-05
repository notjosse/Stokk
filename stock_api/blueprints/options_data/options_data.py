from flask import Blueprint
from flask_login import login_required
from .options_functions import create_signals
from thetadata import ThetaClient, OptionReqType, OptionRight, DateRange

import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt

options_data_bp = Blueprint("options_data", __name__, template_folder="templates")


@options_data_bp.route("/options")
@login_required
def options():

    client = ThetaClient()  # We don't need to provide a username / password because this is a free request.

    with client.connect():  # Make any requests for data inside this block. Requests made outside this block wont run.
        data = client.get_hist_option(
            req=OptionReqType.EOD,
            root="AAPL",
            exp=date(2022, 11, 25),
            strike=150,
            right=OptionRight.CALL,
            date_range=DateRange(dt(2022, 10, 15), dt(2022, 11, 15))
        )
    print(data)

    return {"page": "options"}