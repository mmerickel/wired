def test_greeter():
    from dc.simple_injection.app import App
    from dc.simple_injection.request import process_request

    # start-after
    # Application starts up
    app = App()
    app.scan()

    # Later, a request comes in
    result = process_request(app.registry)
    assert 'Hello Larry my name is Mary.' == result
