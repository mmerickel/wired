from app import App
from configure import register
from request import process_request


def test_greeter():
    # start-after
    app = App()
    register(app.registry)
    result = process_request(app.registry)
    assert 'Hello Larry my name is Mary' == result
