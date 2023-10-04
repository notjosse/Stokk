from flask import Blueprint, render_template, redirect, url_for, flash, request, send_file
from flask_login import login_required, current_user
import requests, json

from stock_api.extensions import api_key


historical_data_bp = Blueprint("historical_data", __name__, template_folder="templates")

# Route to redirect '/home/' --> '/'  
@historical_data_bp.route("/home/", methods=['GET', 'POST'])
def home_home():
    return redirect(url_for('historical_data.home'))

# routes to the home page if route is: '/'
@historical_data_bp.route("/", methods=['GET', 'POST'])
@login_required
def home():

    data = None
    start_date, end_date = None, None

    if request.method == "GET":
        # Historical Data Request

        ticker = request.args.get('stock-query')
        start_date = request.args.get('start-date')
        end_date = request.args.get('end-date')

        # start date must always be less than or equal to the end date
        if start_date and start_date > end_date:
            return render_template('home.html', data=data)

        # If the current user doesn't have enough coins let them know
        if start_date and current_user.get_budget() < 50:
            flash(f'You do not have enough coins to make this request.', category='danger')


        if ticker and len(ticker) <= 4 and current_user.get_budget() >= 50:
            # reduce the budget by 50 coins 
            current_user.reduce_budget()

            # make the request to the nasdaq api
            r = requests.get(f'https://data.nasdaq.com/api/v3/datatables/WIKI/PRICES?date.gte={start_date}&date.lte={end_date}&ticker={ticker}&qopts.columns=date,ticker,open,high,low,close,volume&api_key={api_key}')
            data = r.json()["datatable"]["data"]
            if r.json()["datatable"]["data"] == []:
                data = None

        return render_template('home.html', data=data)


    if request.method == "POST":
    # Download JSON Data:
        export_data = request.form.get('export-json')
        if export_data:
            with open('./stock_api/staging/data.json', 'w', encoding='UTF8') as f:
                json.dump(export_data, f)
                
            return send_file('./staging/data.json', as_attachment=True)

        return redirect(url_for('historical_data.home'))