import pytest
import azure.functions as func
from main import HttpExample

def test_http_example_no_frequency():
    req = func.HttpRequest(
        method='GET',
        url='/api/index.html',
        params={}
    )
    response = HttpExample(req)
    assert response.status_code == 200, "Status code non è 200 per la pagina HTML."
    assert "<html>" in response.get_body().decode(), "Il contenuto HTML non è stato caricato correttamente."
