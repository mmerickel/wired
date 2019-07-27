def test_greeter():
    from dc.injected.app import App
    from dc.injected.request import process_request

    # start-after
    # Application starts up
    app = App()
    app.scan()

    # Later, a request comes in
    results = process_request(app.registry)
    assert 'Hello Billy my name is Mary.' == results[0]
    assert 'Salut Sophie je m\'apelle Henri.' == results[1]
