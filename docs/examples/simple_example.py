from wired import ServiceRegistry


class Greeter:
    def __init__(self, greeting):
        self.greeting = greeting

    def __call__(self):
        return f'{self.greeting} !!'


def app_setup():
    # Make the application's registry
    registry = ServiceRegistry()

    # Greeters are nice...they greet people!
    greeter = Greeter(greeting='Hello')

    # Register it as a singleton using its class for the "key"
    registry.register_singleton(greeter, Greeter)

    return registry


def greet_a_customer(container):

    # Get the registered greeter, do the greeting
    the_greeter = container.get(Greeter)
    greeting = the_greeter()

    return greeting


def main():
    # Setup the application
    registry = app_setup()

    # A customer comes in, handle the steps in the greeting process
    # as a "container".
    container = registry.create_container()
    greeting = greet_a_customer(container)

    # The "request" was handled, return it
    print(greeting)


if __name__ == '__main__':
    main()
