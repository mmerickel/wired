from app import App
from request import process_request


def test_greeter():
    # start-after
    app = App()
    app.scan()
    result = process_request(app.registry)
    assert 'Hello Larry my name is Mary' == result
