def test_greeter():
    from dc.attributes.app import App
    from dc.attributes.request import process_request

    # start-after
    # Application starts up
    app = App()
    app.scan()

    # Later, a request comes in
    results = process_request(app.registry)
    assert 'Hello Billy my name is Mary.' == results[0]
    assert 'Salut Sophie je m\'apelle Henri.' == results[1]
