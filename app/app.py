import logging
import traceback
from modules.extract_data.extract_data_m import (
    stock_screener_call,
    add_fte_call,
    add_yest_soc_sent,
    write_data_to_csv,
)
from modules.update_psql.update_psql_m import conn_to_psql, upload_to_psql
from modules.dash_plotly_dashboard.dash_plotly_dashboard_m import dashboard






def app():
    
    ROW_LIMIT = 10

    # Logging configuration
    logging.basicConfig(
        # filename="logs/app.log",
        handlers=[logging.FileHandler("logs/app.log"), logging.StreamHandler()],
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )
    logging.info("APP STARTED")

    try : 
        # Extract data
        tickers_list, filtered_screener = stock_screener_call(ROW_LIMIT=ROW_LIMIT)
        added_fte = add_fte_call(tickers_list, filtered_screener)
        final_data = add_yest_soc_sent(added_fte, tickers_list)
        write_data_to_csv(final_data)

        # Connect and upload data to PostgreSQL database in GCP
        pool = conn_to_psql()
        upload_to_psql(pool)

        # Generate the dash & plotly web dashboard
        dashboard()
    
    except Exception as e :
        logging.critical(e)
        logging.critical(traceback.format_exc())


if __name__ == "__main__":
    app()
