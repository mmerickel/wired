def test_greeter():
    from dc.overrides.app import App
    from dc.overrides.request import process_request

    # start-after
    # Application starts up
    app = App()
    app.scan()

    # Later, a request comes in
    results = process_request(app.registry)
    assert 'Hello Larry my name is Mary.' == results[0]
    assert 'Salut Anne je m\'apelle Henri.' == results[1]
