def test_greeter():
    from dc.attributes.app import App
    from dc.attributes.request import process_request

    # start-after
    # Application starts up
    app = App()
    app.scan()

    # Later, a request comes in
    result = process_request(app.registry, 'larry')
    assert 'Hello Larry my name is Mary' == result
