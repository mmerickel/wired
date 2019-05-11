from app import make_registry
from main import process_request


def test_greeter():
    registry = make_registry()
    result = process_request(registry)
    assert 'Hello Larry my name is Mary' == result
