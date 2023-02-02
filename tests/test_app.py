import pytest
import pytest_mock
from app.modules.extract_data.extract_data_m import (
    stock_screener_call,
    add_fte_call,
    add_yest_soc_sent,
    write_data_to_csv,
)
from modules.update_psql.update_psql_m import conn_to_psql, upload_to_psql
from modules.dash_plotly_dashboard.dash_plotly_dashboard_m import dashboard


# def test_stock_screener_call():
    
#     #do test