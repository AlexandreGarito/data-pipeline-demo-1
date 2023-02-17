import logging
import traceback
from modules.extract_data.extract_data_m import (
    stock_screener_call,
    add_fte_call,
    add_yest_soc_sent,
    write_data_to_csv,
)
from modules.update_psql.update_psql_m import (
    conn_to_psql,
    upload_to_psql,
    close_conn_to_sql,
)
from modules.dash_plotly_dashboard.dash_plotly_dashboard_m import dashboard


def app():

    ROW_LIMIT = 4

    # Logging configuration
    logging.basicConfig(
        # filename="logs/app.log",
        handlers=[logging.FileHandler("logs/app.log"), logging.StreamHandler()],
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )
    logging.info("APP STARTED")

    try:
        # Extract data
        tickers_list, filtered_screener = stock_screener_call(ROW_LIMIT=ROW_LIMIT)
        added_fte = add_fte_call(tickers_list, filtered_screener)
        final_data = add_yest_soc_sent(added_fte, tickers_list)
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
