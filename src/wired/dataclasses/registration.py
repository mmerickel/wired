from wired import ServiceRegistry, ServiceContainer
from .injector import Injector


def register_dataclass(
        registry: ServiceRegistry,
        target,
        for_=None,
        context=None,
        container: ServiceContainer = None,
):
    """ Generic injectory factory for dataclasses """

    # The common case, for default registrations we can omit
    # the "for_" as it is the same as the class implementing it
    if for_ is None:
        for_ = target

    if getattr(target, 'wired_factory', None):
        # This class wants to control its factory, use that one
        dataclass_factory = target.wired_factory
    else:
        # Use a generic dataclass factory
        def dataclass_factory(c: ServiceContainer):
            injector = Injector(container=c)
            instance = injector(target, context=context)
            return instance

    registry.register_factory(dataclass_factory, for_, context=context)