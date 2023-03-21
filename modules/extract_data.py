"""
This extract_data module uses 4 functions to get data from 3 different API calls.

Functions:
    - screener_call: API call to screen for stocks that we want.
    - screener_transf: API call to get the companies tickers and general data about each company.
    - fte_call: API call to get the full time employees (fte) for each company.
    - add_fte: Adds the full time employees (fte) data.
    - write_data_to_csv : Writes data into final_data.csv
"""


import json
import logging
import os
from datetime import date, timedelta
import pandas as pd
import requests
from modules.gcp_interactions import get_secret


PROJECT_ID = os.environ["PROJECT_ID"]
FMI_API_KEY = get_secret(PROJECT_ID, "FMI_API_KEY")
FINNH_API_KEY = get_secret(PROJECT_ID, "FINNH_API_KEY")
URL_SCREENER = "https://financialmodelingprep.com/api/v3/stock-screener"
URL_FINNHUB = "https://finnhub.io/api/v1/stock/social-sentiment"


def screener_call(row_limit):
    """API call to screen for stocks that we want."""
    logging.info("Stock screener call started.")

    # Two parameters since we can't search for both sectors at the same time.
    PARAMS_TECH = {
        "marketCapMoreThan": 100000000,
        "isActivelyTrading": "true",
        "sector": "Technology",
        "country": "US",
        "exchange": "nasdaq",
        "limit": row_limit,
        "apikey": FMI_API_KEY,
    }

    PARAMS_COM = {
        "marketCapMoreThan": 100000000,
        "sector": "Communication Services",
        "isActivelyTrading": "true",
        "country": "US",
        "exchange": "nasdaq",
        "limit": row_limit,
        "apikey": FMI_API_KEY,
    }

    screener_resp_tech = requests.get(URL_SCREENER, params=PARAMS_TECH)
    screener_resp_com = requests.get(URL_SCREENER, params=PARAMS_COM)

    return screener_resp_tech, screener_resp_com


def screener_transf(row_limit, screener_resp_tech, screener_resp_com):
    """API call to get the companies tickers and general data about each company."""

    tech_data = json.loads(screener_resp_tech.text)
    com_data = json.loads(screener_resp_com.text)

    # Checking if tech_data response is in the expected format:
    if not isinstance(tech_data, list):
        if "Limit Reach" in tech_data["Error Message"]:
            raise Exception("API Limit is reached for financialmodelingprep.com")
        raise Exception("FMI API response data is not in the correct format.")

    tech_data.extend(com_data)
    all_data = tech_data
    sorted_data = sorted(all_data, key=lambda x: x["marketCap"], reverse=True)

    # Eliminate duplicates based on company name, mainly because of Google A and C shares (GOOG and GOOGL)
    unique_sorted_dicts = []
    for d in sorted_data:
        if not any(d["companyName"] == x["companyName"] for x in unique_sorted_dicts):
            unique_sorted_dicts.append(d)

    sorted_data_lim = unique_sorted_dicts[:row_limit]

    # For later use in following API calls
    tickers_list = [d["symbol"] for d in sorted_data_lim]

    filtered_screener = [
        {
            k: v
            for k, v in d.items()
            if k in ["symbol", "companyName", "marketCap", "beta"]
        }
        for d in sorted_data_lim
    ]

    return tickers_list, filtered_screener


def fte_call(tickers_list):
    """API call to get the full time employees (fte) for each company."""

    logging.info("Adding full time employees started.")

    employees_n_list = []

    for ticker in tickers_list:
        URL_PROFILE = f"https://financialmodelingprep.com/api/v3/profile/{ticker}"
        PARAMS = {"apikey": FMI_API_KEY}
        profile_response = requests.get(URL_PROFILE, params=PARAMS)
        profile_response_dict = json.loads(profile_response.text)

        # Checking if profile_response_dict is in the expected format:
        if not isinstance(profile_response_dict, list):
            if "Limit Reach" in profile_response_dict["Error Message"]:
                logging.critical(
                    "API Limit is reached for financialmodelingprep.com, stopping..."
                )
                raise Exception("API Limit is reached for financialmodelingprep.com")
            raise Exception("FMI API response data is not in the correct format.")

        employees_n = [
            {
                k: v
                for k, v in d.items()
                if k in ["symbol", "companyName", "fullTimeEmployees"]
            }
            for d in profile_response_dict
        ]

        # Add the number of employees for this company to the list
        employees_n_list.extend(employees_n)

    # convert the number of employees from a string to an int
    for company in employees_n_list:
        company['fullTimeEmployees'] = int(company['fullTimeEmployees'])
    
    return employees_n_list


def add_fte(employees_n_list, filtered_screener):
    """Adds the full time employees (fte) data."""

    added_fte = [
        {**d1, "fullTimeEmployees": d2["fullTimeEmployees"]}
        for d1, d2 in zip(filtered_screener, employees_n_list)
    ]

    return added_fte


def yest_sent_call(tickers_list):
    """API call to get social media sentiment of the lookback period about each company."""

    logging.info("Adding lookback period's social media sentiment started.")

    # yesterday = date.today() - timedelta(days=1)
    lookback_period = date.today() - timedelta(days=7)
    d_list_sentiment = []

    # Get the sentiment for each ticker
    for ticker in tickers_list:

        twitter_data = None

        params = {
            "symbol": ticker,
            "token": FINNH_API_KEY,
            "from": lookback_period,
            "to": date.today(),
        }
        response_finnhub = requests.get(URL_FINNHUB, params=params)
        json_data = response_finnhub.json()

        # Sometimes companies don't have twitter mentions
        # logging.info(f"json_data : {json_data}")
        # FIXME: Following Twitter API not being free anymore, Finnhub.com ceased to provide twitter data
        # FIXME: so, switching to reddit, even though the data is very scarce
        if json_data["reddit"]:
            twitter_data = json_data["reddit"]
        if twitter_data:
            sentiment_summary = {
                "yest_twitter_positive_mentions": sum(
                    x["positiveMention"] for x in twitter_data
                ),
                "yest_twitter_negative_mentions": sum(
                    x["negativeMention"] for x in twitter_data
                ),
                "yest_twitter_mean_sentiment_score": sum(
                    x["score"] for x in twitter_data
                )
                / len(twitter_data),
            }
        else:
            sentiment_summary = {}

        d_list_sentiment.append(sentiment_summary)
        
    return d_list_sentiment

def add_yest_sent(added_fte, d_list_sentiment):
    """Adds the sentiment data"""
    for i, d in enumerate(added_fte):
        try:
            added_fte[i].update(d_list_sentiment[i])
        except IndexError:
            pass

    final_data = added_fte

    return final_data


def write_data_to_csv(final_data):

    logging.info("Writing final data to csv...")

    name_final_data_csv = os.path.join('data', "final_data.csv")
    df_final_data = pd.DataFrame(final_data)
    df_final_data.to_csv(name_final_data_csv)

    logging.info("Final data written to {}.".format(name_final_data_csv))
