import pytest
from jsonschema import validate
import pandas as pd
import json  
from main import calculate_returns

returns_schema = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "date": {"type": "string"},
            "close": {"type": "number"},
            "Return": {"type": ["number", "null"]}  
        },
        "required": ["date", "close", "Return"]
    }
}

def test_calculate_returns_contract():
  
    data = {
        'date': ['2020-01-01', '2020-01-02', '2020-01-03'],
        'close': [100, 101, 102]
    }
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date']) 
    df_returns = calculate_returns(df, 'daily')
    assert df_returns is not None, "La funzione dovrebbe restituire un DataFrame"

    data_json = df_returns.reset_index().to_json(orient='records', date_format='iso')
    data_parsed = json.loads(data_json)

    validate(instance=data_parsed, schema=returns_schema)
