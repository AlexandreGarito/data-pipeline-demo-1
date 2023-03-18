import os
import tempfile
from unittest.mock import Mock, patch, MagicMock
import requests
import json
from main import (
    screener_call,
    screener_transf,
    fte_call,
    add_fte,
    yest_sent_call,
    add_yest_sent,
    write_data_to_csv,
    conn_to_psql,
    upload_to_psql,
    close_conn_to_sql,
    dashboard,
)


ROW_LIMIT = 3


def test_row_limit():
    """Test if ROW_LIMIT is compatible with the script by being an integer > 0"""

    assert ROW_LIMIT > 0
    assert isinstance(ROW_LIMIT, int)


def test_screener_call():
    """Test the screener API call, and check if responses are present and conforming to expectations."""

    screener_resp_tech, screener_resp_com = screener_call(ROW_LIMIT)

    assert isinstance(screener_resp_tech, requests.Response)
    assert isinstance(screener_resp_com, requests.Response)

    for company_dict in json.loads(screener_resp_tech.text):
        assert company_dict["sector"] == "Technology"
    for company_dict in json.loads(screener_resp_com.text):
        assert company_dict["sector"] == "Communication Services"


def test_screener_transf():
    """Test the data transformations from mock API data."""

    mock_screener_resp_tech = Mock()
    mock_screener_resp_tech.text = json.dumps(
        [
            {
                "symbol": "AAPL",
                "companyName": "Apple Inc.",
                "marketCap": 2435465032520,
                "sector": "Technology",
                "industry": "Consumer Electronics",
                "beta": 1.277894,
                "price": 153.93,
                "lastAnnualDividend": 0.91,
                "volume": 21369134,
                "exchange": "NASDAQ Global Select",
                "exchangeShortName": "NASDAQ",
                "country": "US",
                "isEtf": False,
                "isActivelyTrading": True,
            },
            {
                "symbol": "MSFT",
                "companyName": "Microsoft Corporation",
                "marketCap": 1989057815101,
                "sector": "Technology",
                "industry": "Software—Infrastructure",
                "beta": 0.91562,
                "price": 267.21,
                "lastAnnualDividend": 2.54,
                "volume": 9842191,
                "exchange": "NASDAQ Global Select",
                "exchangeShortName": "NASDAQ",
                "country": "US",
                "isEtf": False,
                "isActivelyTrading": True,
            },
            {
                "symbol": "NVDA",
                "companyName": "NVIDIA Corporation",
                "marketCap": 554993320000,
                "sector": "Technology",
                "industry": "Semiconductors",
                "beta": 1.790446,
                "price": 222.71,
                "lastAnnualDividend": 0.16,
                "volume": 18605246,
                "exchange": "NASDAQ Global Select",
                "exchangeShortName": "NASDAQ",
                "country": "US",
                "isEtf": False,
                "isActivelyTrading": True,
            },
        ]
    )

    mock_screener_resp_com = Mock()
    mock_screener_resp_com.text = json.dumps(
        [
            {
                "symbol": "GOOGL",
                "companyName": "Alphabet Inc.",
                "marketCap": 1219301240387,
                "sector": "Communication Services",
                "industry": "Internet Content & Information",
                "beta": 1.085774,
                "price": 95.07,
                "lastAnnualDividend": 0,
                "volume": 13068379,
                "exchange": "NASDAQ Global Select",
                "exchangeShortName": "NASDAQ",
                "country": "US",
                "isEtf": False,
                "isActivelyTrading": True,
            },
            {
                "symbol": "GOOG",
                "companyName": "Alphabet Inc.",
                "marketCap": 1217236637842,
                "sector": "Communication Services",
                "industry": "Internet Content & Information",
                "beta": 1.085774,
                "price": 95.2,
                "lastAnnualDividend": 0,
                "volume": 11183857,
                "exchange": "NASDAQ Global Select",
                "exchangeShortName": "NASDAQ",
                "country": "US",
                "isEtf": False,
                "isActivelyTrading": True,
            },
            {
                "symbol": "META",
                "companyName": "Meta Platforms, Inc.",
                "marketCap": 455837967789,
                "sector": "Communication Services",
                "industry": "Internet Content & Information",
                "beta": 1.220013,
                "price": 175.82,
                "lastAnnualDividend": 0,
                "volume": 9431931,
                "exchange": "NASDAQ Global Select",
                "exchangeShortName": "NASDAQ",
                "country": "US",
                "isEtf": False,
                "isActivelyTrading": True,
            },
        ]
    )

    tickers_list, filtered_screener = screener_transf(
        row_limit=ROW_LIMIT,
        screener_resp_tech=mock_screener_resp_tech,
        screener_resp_com=mock_screener_resp_com,
    )

    assert len(tickers_list) == ROW_LIMIT
    # Test for duplicate tickers
    # set(list) create a set from a list that removes any duplicate elements since sets only contain unique elements.
    assert len(tickers_list) == len(set(tickers_list))
    for ticker in tickers_list:
        assert ticker.isupper()
    # Test if filtered_screener is a list of dicts
    assert isinstance(filtered_screener, list) and all(
        isinstance(d, dict) for d in filtered_screener
    )
    assert filtered_screener[0]["symbol"] == "AAPL"
    assert filtered_screener[0]["marketCap"] == 2435465032520


def test_fte_call():
    """Test the full time employees API call, and check if responses are present and conforming to expectations."""

    mock_tickers_list = ["AAPL", "MSFT", "GOOG", "META", "NVDA"]

    employees_n_list = fte_call(tickers_list=mock_tickers_list)

    assert isinstance(employees_n_list, list)
    assert employees_n_list[0]["symbol"].isupper()
    assert employees_n_list[0]["fullTimeEmployees"] > 0


def test_add_fte():
    """Test adding the full time employees data from mock API data."""

    mock_employees_n_list = [
        {
            "symbol": "AAPL",
            "companyName": "Apple Inc.",
            "fullTimeEmployees": 164000,
        },
        {
            "symbol": "MSFT",
            "companyName": "Microsoft Corporation",
            "fullTimeEmployees": 221000,
        },
        {
            "symbol": "GOOGL",
            "companyName": "Alphabet Inc.",
            "fullTimeEmployees": 186779,
        },
    ]

    mock_filtered_screener = [
        {
            "symbol": "AAPL",
            "companyName": "Apple Inc.",
            "marketCap": 2413630810829,
            "beta": 1.277894,
        },
        {
            "symbol": "MSFT",
            "companyName": "Microsoft Corporation",
            "marketCap": 1920947044516,
            "beta": 0.91562,
        },
        {
            "symbol": "GOOGL",
            "companyName": "Alphabet Inc.",
            "marketCap": 1209774636989,
            "beta": 1.085774,
        },
    ]

    added_fte = add_fte(
        employees_n_list=mock_employees_n_list,
        filtered_screener=mock_filtered_screener,
    )

    assert isinstance(added_fte, list)
    assert added_fte[0]["symbol"] == "AAPL"
    assert added_fte[0]["marketCap"] == 2413630810829
    assert added_fte[0]["fullTimeEmployees"] == 164000


def test_yest_sent_call():
    """Test yesterday social sentiment API call, and check if responses are present and conforming to expectations."""

    mock_tickers_list = ["AAPL", "MSFT", "GOOG", "META", "NVDA"]
    d_list_sentiment = yest_sent_call(tickers_list=mock_tickers_list)

    assert isinstance(d_list_sentiment, list)
    # assert d_list_sentiment[0]["yest_twitter_positive_mentions"] >= 0


def test_add_yest_sent():
    """Test adding the yesterday social sentiment data from mock API data."""

    mock_added_fte = [
        {
            "symbol": "AAPL",
            "companyName": "Apple Inc.",
            "marketCap": 2413630810829,
            "beta": 1.277894,
            "fullTimeEmployees": 164000,
        },
        {
            "symbol": "MSFT",
            "companyName": "Microsoft Corporation",
            "marketCap": 1920947044516,
            "beta": 0.91562,
            "fullTimeEmployees": 221000,
        },
        {
            "symbol": "GOOGL",
            "companyName": "Alphabet Inc.",
            "marketCap": 1209774636989,
            "beta": 1.085774,
            "fullTimeEmployees": 186779,
        },
    ]

    mock_d_list_sentiment = [
        {
            "yest_twitter_positive_mentions": 635,
            "yest_twitter_negative_mentions": 734,
            "yest_twitter_mean_sentiment_score": -0.1396835036534542,
        },
        {
            "yest_twitter_positive_mentions": 454,
            "yest_twitter_negative_mentions": 448,
            "yest_twitter_mean_sentiment_score": 0.0690662677249494,
        },
        {
            "yest_twitter_positive_mentions": 246,
            "yest_twitter_negative_mentions": 333,
            "yest_twitter_mean_sentiment_score": -0.17537234188129472,
        },
    ]

    final_data = add_yest_sent(
        added_fte=mock_added_fte,
        d_list_sentiment=mock_d_list_sentiment,
    )

    assert isinstance(final_data, list)
    assert final_data[0]["symbol"] == "AAPL"
    assert final_data[0]["marketCap"] == 2413630810829
    assert final_data[0]["fullTimeEmployees"] == 164000
    assert final_data[0]["yest_twitter_positive_mentions"] == 635


def test_write_data_to_csv():
    """Test if data is properly written"""

    with tempfile.TemporaryDirectory() as tmpdir:

        final_data = [
            {
                "symbol": "AAPL",
                "companyName": "Apple Inc.",
                "marketCap": 2413630810829,
                "beta": 1.277894,
                "fullTimeEmployees": 164000,
                "yest_twitter_positive_mentions": 635,
                "yest_twitter_negative_mentions": 734,
                "yest_twitter_mean_sentiment_score": -0.1396835036534542,
            },
            {
                "symbol": "MSFT",
                "companyName": "Microsoft Corporation",
                "marketCap": 1920947044516,
                "beta": 0.91562,
                "fullTimeEmployees": 221000,
                "yest_twitter_positive_mentions": 454,
                "yest_twitter_negative_mentions": 448,
                "yest_twitter_mean_sentiment_score": 0.0690662677249494,
            },
            {
                "symbol": "GOOGL",
                "companyName": "Alphabet Inc.",
                "marketCap": 1209774636989,
                "beta": 1.085774,
                "fullTimeEmployees": 186779,
                "yest_twitter_positive_mentions": 246,
                "yest_twitter_negative_mentions": 333,
                "yest_twitter_mean_sentiment_score": -0.17537234188129472,
            },
        ]

        write_data_to_csv(final_data)

        # check that the file was created in the temporary folder
        filename = os.path.join("data", "final_data.csv")
        print("Temporary directory:", tmpdir)
        print("File path:", filename)
        print("File exists?", os.path.exists(filename))
        assert os.path.exists(filename)


@patch("sqlalchemy.create_engine")
def test_conn_to_psql(mock_create_engine):
    """Test if sqlalchemy.create_engine is properly called"""

    mock_engine = Mock()
    mock_create_engine.return_value = mock_engine
    pool, connector = conn_to_psql()

    mock_create_engine.assert_called_once()
    assert pool is not None
    assert connector is not None


@patch("pandas.DataFrame.to_sql")
def test_upload_to_psql(mock_to_sql):
    """Test if .to_sql is properly called in the function"""

    pool = MagicMock()
    upload_to_psql(pool)

    # assert that to_sql method was called
    mock_to_sql.assert_called_once()


@patch("google.cloud.sql.connector.Connector")
@patch("sqlalchemy.create_engine")
def test_close_conn_to_sql(mock_connector, mock_pool):
    """Test if connection closing is called"""

    mock_connector.return_value = MagicMock()
    mock_pool = MagicMock()

    close_conn_to_sql(mock_pool, mock_connector)

    assert mock_connector.close.called
    assert mock_pool.dispose.called


@patch("dash.Dash.run_server")
def test_dashboard(mock_run_server):
    """Test if app.run_server is called"""

    mock_run_server.return_value = MagicMock()

    dashboard()

    assert mock_run_server.called
