# app.py


def test_greeter():
    from dc.simple_construction.app import App
    from dc.simple_construction.configure import register
    from dc.simple_construction.request import process_request

    # start-after
    # Application starts up
    app = App()
    register(app.registry)

    # Later, a request comes in
    result = process_request(app.registry)
    assert 'Hello Larry my name is Mary' == result
