def test_greeter():
    from dc.singleton.app import App
    from dc.singleton.request import process_request

    # start-after
    # Application starts up
    app = App()
    app.scan()

    # Later, a request comes in
    result = process_request(app.registry)
    assert 'Hello Larry my name is Mary.' == result
