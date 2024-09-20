from jsonschema import validate

schema = {
    "type" : "object",
    "properties" : {
        "price" : {"type" : "number"},
        "name" : {"type" : "string"},
    },
}


      # content of test_sample.py
def func(x):
    return x + 1


def test_answer():
    assert func(3) == 4

def test_json_succes():
    validate(instance={"name" : "Eggs", "price" : 34.99}, schema=schema)