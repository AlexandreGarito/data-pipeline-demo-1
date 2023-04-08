""" The main script perform the following steps:
- Determine the amount of rows (ROW_LIMIT) to filter on the company stock screener. This determines the amount of data 
called on the APIs and displayed on the dashboard charts.
- Configure logging settings
- Extract and transform the data from the APIs
- Write the transformed data to a csv file
- Upload the data to a GCP Cloud SQL PostgreSQL database (serves no purpose at the moment, mainly to practice 
my ability to connect and upload)
- Execute sample queries to verify the proper insertion of data
- Close the database connection
- Generate the Dash Plotly dashboard webserver and run it on the open port of the GCP Cloud Run container.
"""

import logging
import traceback
from modules.extract_data import (
    screener_call,
    screener_transf,
    fte_call,
    add_fte,
    yest_sent_call,
    add_yest_sent,
    write_data_to_csv,
)
from modules.update_psql import (
    conn_to_psql,
    upload_to_psql,
    close_conn_to_sql,
)
from modules.dash_plotly_dashboard import dashboard


ROW_LIMIT = 12


def app():
    """Global app"""

    # Logging configuration
    logging.basicConfig(
        # filename="logs/app.log",
        handlers=[logging.FileHandler("logs/app.log"), logging.StreamHandler()],
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )
    logging.info("APP STARTED")

    try:
        # API calls data extraction & transformation
        screener_resp_tech, screener_resp_com = screener_call(row_limit=ROW_LIMIT)
        tickers_list, filtered_screener = screener_transf(
            row_limit=ROW_LIMIT,
            screener_resp_tech=screener_resp_tech,
            screener_resp_com=screener_resp_com,
        )

        employees_n_list = fte_call(tickers_list)
        added_fte = add_fte(employees_n_list, filtered_screener)

        d_list_sentiment = yest_sent_call(tickers_list)
        final_data = add_yest_sent(added_fte, d_list_sentiment)
        write_data_to_csv(final_data)

        # Connect to database, upload data, and close the connection.
        pool, connector = conn_to_psql()
        upload_to_psql(pool)
        close_conn_to_sql(pool, connector)

        # Generate the dash & plotly web dashboard
        dashboard()

    except Exception as e:
        logging.critical(e)
        logging.critical(traceback.format_exc())


if __name__ == "__main__":
    app()
