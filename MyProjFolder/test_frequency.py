import pytest
import azure.functions as func
from main import HttpExample

def test_http_example_no_frequency():
    req = func.HttpRequest(
        method='GET',
        url='/api/index.html',
        params={},
        body=b""
    )
    response = HttpExample(req)
    assert response.status_code == 200, "Status code non è 200 per la pagina HTML."
    
    html_content = response.get_body().decode()
    print("HTML Content:", html_content)
