def test_greeter():
    from dc.custom_factories.app import App
    from dc.custom_factories.request import process_request

    # start-after
    # Application starts up
    app = App()
    app.scan()

    # Later, a request comes in
    result = process_request(app.registry, 'larry')
    assert 'Hello my name is Mary' == result
