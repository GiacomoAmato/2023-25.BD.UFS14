from jsonschema import validate
from main import get_initial_response, get_second_response, extract_ingredients
from main import get_ingredient_report, extract_pdf_link, download_pdf, get_paging_cookie

url = "https://cir-reports.cir-safety.org/"
schema = {
    "$schema": "http://json-schema.org/draft-06/schema#",
    "$ref": "#/definitions/Welcome",
    "definitions": {
        "Welcome": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "pcpc_ingredientid": {
                    "type": "string",
                    "format": "uuid"
                },
                "pcpc_ingredientname": {
                    "type": "string"
                },
                "pcpc_ciringredientid": {
                    "type": "string",
                    "format": "uuid"
                },
                "pcpc_ciringredientname": {
                    "type": "string"
                },
                "pcpc_cirreportname": {
                    "type": "string"
                }
            },
            "required": [
                "pcpc_ciringredientid",
                "pcpc_ciringredientname",
                "pcpc_cirreportname",
                "pcpc_ingredientid",
                "pcpc_ingredientname"
            ],
            "title": "Welcome"
        }
    }
}

def test_get_initial_response():
    response = get_initial_response(url)
    assert response.status_code == 200

cookie = get_paging_cookie(get_initial_response(url))

def test_get_second_response():
    response = get_second_response(url + "FetchCIRReports/", cookie)
    assert response.status_code == 200

def test_extract_ingredients():
    catalogo = extract_ingredients("json1", "json2")
    assert validate_wrapper(catalogo, schema) == True

def validate_wrapper(instance, schema):
    try:
        validate(instance=instance, schema=schema)
        return True
    except:
        return False

html_contenuto = get_ingredient_report(url, "940af697-52b5-4a3a-90a6-b9db30ef4a7e")

def test_extract_pdf_link():
    link_pdf = extract_pdf_link(html_contenuto)
    #snapshot link ingredient per il pdf



"""
def test_extract_ingredients():
    documento1 = [{"pcpc_ingredientname": "Ing1", "pcpc_ciringredientid": "ID1"}]
    documento2 = [{"pcpc_ingredientname": "Ing2", "pcpc_ciringredientid": "ID2"}]
    ingredienti, nomi = extract_ingredients(documento1, documento2)
    assert len(ingredienti) == 2
    assert "Ing1" in nomi and "Ing2" in nomi

"""