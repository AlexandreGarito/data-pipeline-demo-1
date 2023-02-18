"""
This extract_data module uses 4 functions to get data from 3 different API calls.

Functions:
    - stock_screener_call : Filters for the companies tickers and get general data about each company.
    - add_fte_call : Adds the numbers of employees for each company.
    - add_yest_soc_sent : Adds yesterday's social twitter sentiment about each company.
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



def stock_screener_call(ROW_LIMIT):
    """stock_screener_call filters for the companies tickers and get general data about each company."""

    logging.info("Stock screener call started.")
    
    # Two parameters since we can't search for both sectors at the same time.
    PARAMS_TECH = {
        "marketCapMoreThan": 100000000,
        "isActivelyTrading": "true",
        "sector": "Technology",
        "country": "US",
        "exchange": "nasdaq",
        "limit": ROW_LIMIT,
        "apikey": FMI_API_KEY,
    }

    PARAMS_COM = {
        "marketCapMoreThan": 100000000,
        "sector": "Communication Services",
        "isActivelyTrading": "true",
        "country": "US",
        "exchange": "nasdaq",
        "limit": ROW_LIMIT,
        "apikey": FMI_API_KEY,
    }

    response_tech = requests.get(URL_SCREENER, params=PARAMS_TECH)
    response_com = requests.get(URL_SCREENER, params=PARAMS_COM)

    tech_data = json.loads(response_tech.text)
    com_data = json.loads(response_com.text)
    
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

    sorted_data_lim = unique_sorted_dicts[:ROW_LIMIT]

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


def add_fte_call(tickers_list, filtered_screener):
    """add_fte_call adds the full time employees (fte) for each company."""
    
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
                logging.critical("API Limit is reached for financialmodelingprep.com, stopping...")
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

    # Merge the previously created filtered general data with the full time employees data
    added_fte = [
        {**d1, "fullTimeEmployees": d2["fullTimeEmployees"]}
        for d1, d2 in zip(filtered_screener, employees_n_list)
    ]

    return added_fte


def add_yest_soc_sent(added_fte, tickers_list):
    """add_yest_soc_sent adds yesterday's social twitter sentiment about each company."""

    logging.info("Adding yesterday's twitter social sentiment started.")
    
    yesterday = date.today() - timedelta(days=1)

    URL_FINNHUB = "https://finnhub.io/api/v1/stock/social-sentiment"

    d_list_sentiment = []

    # Get the sentiment for each ticker
    for ticker in tickers_list:
        
        twitter_data = None
        
        params = {
            "symbol": ticker,
            "token": FINNH_API_KEY,
            "from": yesterday,
            "to": date.today(),
        }
        response_finnhub = requests.get(URL_FINNHUB, params=params)
        json_data = response_finnhub.json()
        
        # Sometimes companies don't have twitter mentions
        if json_data["twitter"]:
            twitter_data = json_data["twitter"]
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

    # Add the sentiment dicts to the added_fte list of dicts
    for i, d in enumerate(added_fte):
        try :
            added_fte[i].update(d_list_sentiment[i])
        except IndexError: pass
        
    final_data = added_fte

    return final_data


def write_data_to_csv(final_data):
    
    logging.info("Writing final data to csv...")
    
    name_final_data_csv = "data/final_data.csv"
    df_final_data = pd.DataFrame(final_data)
    df_final_data.to_csv(name_final_data_csv)
    
    logging.info("Final data written to {}.".format(name_final_data_csv))
