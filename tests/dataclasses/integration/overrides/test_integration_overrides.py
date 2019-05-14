
def test_greeter():
    # start-after
    # Application starts up
    from app import App
    from request import process_request

    app = App()
    app.scan()
    # Later, a request comes in
    results = process_request(app.registry)
    assert 'Hello Larry my name is Mary.' == results[0]
    assert 'Salut Anne je m\'apelle Henri.' == results[1]
