import pytest
import pandas as pd
from main import calculate_returns

def test_calculate_returns_values():
   
    data = {
        'date': pd.date_range(start='2020-01-01', periods=5, freq='D'),
        'close': [100, 105, 110, 115, 120]
    }
    df = pd.DataFrame(data)
    df_returns = calculate_returns(df, 'daily')
    assert df_returns is not None, "La funzione dovrebbe restituire un DataFrame"

    expected_returns = df['close'].pct_change()
    expected_returns = expected_returns[::5]  
    pd.testing.assert_series_equal(df_returns['Return'], expected_returns, check_names=False)
