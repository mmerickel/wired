"""

A customer walks into a store. Do the steps to interact with them:

- Get a correct greeter

- Interact with them

Simple wired application:

- Settings that say what punctuation to use

- Registry

- A bundled Greeter and Customer

- An add-on which defines a FrenchGreeter and FrenchCustomer

- A Datastore which stores/retrieves instances of Customers

- Request and View factories to assemble the full processing chain

"""
from typing import List

from wired import ServiceRegistry
from .models import (
    Customer,
    Datastore,
    Greeter,
    Resource,
    Request,
    Settings,
    Url,
    View,
)


def app_bootstrap(settings: Settings) -> ServiceRegistry:
    # Make the registry
    registry = ServiceRegistry()

    # Do setup for the core application features
    setup(registry, settings)

    # Import the add-on and initialize it
    from .custom import setup as addon_setup

    addon_setup(registry, settings)

    return registry


def setup(registry: ServiceRegistry, settings: Settings):
    """ Initialize the features in the core application  """

    # Make and register the Datastore singleton
    datastore = Datastore()
    registry.register_singleton(datastore, Datastore)

    # Context factory
    def context_factory(container) -> Resource:
        # Presumes that "url" is in the container
        ds: Datastore = container.get(Datastore)
        url: str = container.get(Url)
        context: Resource = ds.customers.get(url)
        return context

    registry.register_factory(context_factory, Resource)

    # Request factory
    def request_factory(container) -> Request:
        url: str = container.get(Url)
        request = Request(url=url, container=container)
        return request

    registry.register_factory(request_factory, Request)

    # **** Default View
    def view_factory(container) -> View:
        request: Request = container.get(Request)
        context: Resource = container.get(Resource)
        greeter: Greeter = container.get(Greeter, context=context)
        view = View(request=request, context=context, greeter=greeter)
        return view

    registry.register_factory(view_factory, View)

    # **** Default Greeter
    def default_greeter_factory(container) -> Greeter:
        # Use the dataclass default for greeting
        return Greeter(punctuation=settings.punctuation)

    # Register it as a factory using its class for the "key"
    registry.register_factory(default_greeter_factory, Greeter)

    # During bootstrap, make some Customers
    mary = Customer(name='mary', title='Mary')
    datastore.customers['mary'] = mary


def process_request(registry: ServiceRegistry, url: str) -> str:
    """ Given URL (customer name), make a Request to handle interaction """

    # Make the container that this request gets processed in
    container = registry.create_container()

    # Put the url into the container
    container.register_singleton(url, Url)

    # Create a View to generate the greeting
    view = container.get(View)

    # Generate a response
    response = view()

    return response


def sample_interactions(registry: ServiceRegistry) -> List[str]:
    """ Pretend to do a couple of customer interactions """

    return [process_request(registry, url) for url in ('mary', 'henri')]


def main():
    settings = Settings(punctuation='!!')
    registry = app_bootstrap(settings)
    greetings = sample_interactions(registry)
    assert greetings == ['Hello Mary !!', 'Bonjour Henri !!']


if __name__ == '__main__':
    main()
