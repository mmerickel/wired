from wired import ServiceRegistry, ServiceContainer
from .injector import Injector


def register_dataclass(
    registry: ServiceRegistry, target, for_=None, context=None
):
    """ Generic injector factory for dataclasses """

    # The common case, for default registrations we can omit
    # the "for_" as it is the same as the class implementing it
    if for_ is None:
        for_ = target

    # Use a generic dataclass factory
    def dataclass_factory(container: ServiceContainer):
        injector = Injector(container=container)
        instance = injector(target)
        return instance

    registry.register_factory(dataclass_factory, for_, context=context)
