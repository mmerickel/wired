
def test_greeter():
    from dc.injected.app import App
    from dc.injected.request import process_request

    # start-after
    # Application starts up
    app = App()
    app.scan()

    # Later, a request comes in
    result = process_request(app.registry, 'larry')
    assert 'Hello Larry my name is Mary' == result
