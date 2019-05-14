def xxx_test_greeter():
    # start-after
    # Application starts up
    from app import App
    from request import process_request

    app = App()
    app.scan()
    # Later, a request comes in
    result = process_request(app.registry, 'larry')
    assert 'Hello Larry my name is Mary' == result
