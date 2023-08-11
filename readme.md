# Stokk

This app will return data on queried stock market tickers.
The backend will call the Nasdaq api to fetch financial data.

## Import Requirements

To import requirements for this app, use the following `pip` commands:

- `pip install -r requirements.txt`

or

- `python -m pip install -r requirements.txt`

If using python3:
- `python3 -m pip install -r requirements.txt`

## Export Requirements

To export any newly added requirements and maintain the requirements.txt file, use the following `pip` command:

- `pip freeze > requirements.txt`

or

- `python -m pip freeze > requirements.txt`

If using python3:
- `python3 -m pip freeze > requirements.txt`

## Nasdaq API Key

If you have a Nasdaq api key and would like to use it when sending get requests, do the following:

1. Create a new file in the root directory called `api_key.json`
2. In the file, create a json objects as follows:
    - {"key": "<your_actual_api_key>"}
    - replace `<you_actual_api_key>` with your Nasdaq api key string

If you don't have an api key, a free one can be generated at: https://data.nasdaq.com/