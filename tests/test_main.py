# import pytest
from app.modules.extract_data.extract_data_m import (
    cacacoco,
    # stock_screener_call,
    # add_fte_call,
    # add_yest_soc_sent,
    # write_data_to_csv,
)
from app.modules.update_psql.update_psql_m import conn_to_psql, upload_to_psql
from app.modules.dash_plotly_dashboard.dash_plotly_dashboard_m import dashboard

from unittest.mock import patch
import unittest





# # Define the function we want to test
# def my_function():
#     print("caca")

# Define a test for the function using the patch decorator
@patch("app.modules.extract_data.extract_data_m.cacacoco")
def test_cacacoco(mock_function):
    # Set the return value of the mock function
    mock_function.return_value = 42

    # Call the function we want to test
    result = cacacoco()

    # Verify that the mock function was called with the correct arguments
    mock_function.assert_called_once()

    # Verify that the result is the expected value
    assert result == 42
    
    

if __name__ == '__main__':
    unittest.main()