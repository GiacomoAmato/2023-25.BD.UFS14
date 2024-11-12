import pytest
import azure.functions as func
import os
from main import HttpExample

def test_http_example_file_not_found():
    csv_path = os.path.join(os.path.dirname(__file__), 'GLD_data_AV_clean_no_outliers.csv')
    # Rinomina temporaneamente il file CSV per simulare l'assenza del file
    os.rename(csv_path, csv_path + "_backup")
    
    req = func.HttpRequest(
        method='GET',
        url='/api/index.html',
        params={'frequency': 'daily'}
    )
    response = HttpExample(req)
    
    assert response.status_code == 500, "Status code non è 500 quando il file CSV è mancante."
    assert "File CSV non trovato" in response.get_body().decode(), "Messaggio di errore non corrisponde quando il file CSV è mancante."
    
    # Ripristina il file CSV
    os.rename(csv_path + "_backup", csv_path)
