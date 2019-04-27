from typing import get_type_hints

from wired import ServiceRegistry, ServiceContainer
from .models import View, Url


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


def injector_construction(container: ServiceContainer, target):
    """ Introspect dataclass and get arguments from container """

    # Make the args dict that we will construct dataclass with
    args = {}

    # Iterate through the dataclass fields
    for field_name, field_type in get_type_hints(target).items():
        if field_type != str:
            args[field_name] = container.get(field_type)

    # Now construct an instance of the target dataclass
    return target(**args)


def register_dataclass(registry: ServiceRegistry, target, for_, context=None):
    """ Generic injectory factory for dataclasses """

    # Note: This function could be a decorator which already knows
    # the registry, has all the targets, and can do them in one
    # container that it makes. For example:
    # from wired.decorators import factory
    # @factory(for_=Greeter, context=FrenchCustomer)
    # @datclass
    # class FrenchGreeter(Greeter):
    #   pass

    if getattr(target, 'factory', None):
        # This class wants to control its factory, use that one
        dataclass_factory = target.factory
    else:
        # Use a generic dataclass factory
        def dataclass_factory(c: ServiceContainer):
            instance = injector_construction(c, target)
            return instance

    registry.register_factory(dataclass_factory, for_, context=context)
