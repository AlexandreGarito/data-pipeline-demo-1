"""
This update_psql module uses 2 functions to connect and update to the GCP Cloud SQL PostgreSQL database.

Functions:
    - conn_to_psql : Connects to the GCP Cloud SQL PostgreSQL database.
    - upload_to_psql : Uploads data to the GCP Cloud SQL PostgreSQL database.
"""


import logging

import os
from google.cloud.sql.connector import Connector
import pandas as pd
import sqlalchemy
from modules.gcp_interactions.secret_manager import get_secret


PROJECT_ID = os.environ["PROJECT_ID"]
SQL_INSTANCE_CONNECTION_NAME1 = get_secret(PROJECT_ID, "SQL_INSTANCE_CONNECTION_NAME1")
SQL_DB_USER1 = get_secret(PROJECT_ID, "SQL_DB_USER1")
SQL_DB_PASS1 = get_secret(PROJECT_ID, "SQL_DB_PASS1")
SQL_DB_NAME1 = get_secret(PROJECT_ID, "SQL_DB_NAME1")
SQL_DB_TABLE_NAME1 = get_secret(PROJECT_ID, "SQL_DB_TABLE_NAME1")


def conn_to_psql():
    """Connects to the GCP Cloud SQL PostgreSQL database"""
    
    logging.info("Connecting to database...")
    
    connector = Connector()

    def getconn_SQL():
        conn = connector.connect(
            SQL_INSTANCE_CONNECTION_NAME1,
            "pg8000",
            user=SQL_DB_USER1,
            password=SQL_DB_PASS1,
            db=SQL_DB_NAME1,
        )
        return conn

    # create connection pool with 'creator' argument to our connection object
    try:
        pool = sqlalchemy.create_engine(
            "postgresql+pg8000://",
            creator=getconn_SQL,
        )
        logging.info("Connection successfull!")
    except:
        logging.warning("Connection to GCP database failed!")
        
    return pool, connector


def upload_to_psql(pool):
    """Upload data to the GCP Cloud SQL PostgreSQL database"""
    
    logging.info("Uploading data to GCP database...")
    
    df_final_data = pd.read_csv("final_data.csv")
    df_final_data.to_sql(SQL_DB_TABLE_NAME1, pool, if_exists="replace", index=False)

    # Verify data has been inserted
    query = f"SELECT * FROM {SQL_DB_TABLE_NAME1}"
    result = pd.read_sql(query, pool)
    if result is not None:
        logging.info("Data inserted.")
    print("SQL query result : \n")
    print(result)

def close_conn_to_sql(pool, connector):
    """Closes the connection to the GCP Cloud SQL PostgreSQL database"""
    
    logging.info("Closing connection to database...")
    
    connector.close() # clean up the Connector object only used to authenticate the user
    pool.dispose() # close the database connections managed by the connection pool
    
    logging.info("Connection closed.")