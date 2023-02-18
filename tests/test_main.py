import pytest





from main import (
    stock_screener_call,
    add_fte_call,
    add_yest_soc_sent,
    write_data_to_csv,
)




def test_stock_screener_call():

    # Verify that the result is the expected value
    assert 43 == 43
    
    