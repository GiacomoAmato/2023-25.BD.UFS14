import pytest
import azure.functions as func
import os
from main import HttpExample

def test_http_example_file_not_found():
    csv_path = os.path.join(os.path.dirname(__file__), 'GLD_data_AV_clean_no_outliers.csv')
    
    if not os.path.exists(csv_path):
        with open(csv_path, 'w') as f:
            f.write('date,close\n2023-01-01,100\n2023-01-02,101\n')  # Dati di prova

    os.rename(csv_path, csv_path + "_backup")
    
    req = func.HttpRequest(
        method='GET',
        url='/api/index.html',
        params={'frequency': 'daily'},
        body=b""
    )
    response = HttpExample(req)
    
    assert response.status_code == 500, "Status code non è 500 quando il file CSV è mancante."
    assert "File CSV non trovato" in response.get_body().decode(), "Messaggio di errore non corrisponde quando il file CSV è mancante."
    
    os.rename(csv_path + "_backup", csv_path)
