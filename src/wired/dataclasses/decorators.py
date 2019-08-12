from venusian import attach, Scanner
from wired import ServiceRegistry

from .registration import register_dataclass


# noinspection PyPep8Naming
class singleton:
    def __init__(self, for_=None, context=None, name: str = None):
        self.for_ = for_
        self.context = context if context else for_
        self.name = name

    def __call__(self, wrapped):
        def callback(scanner: Scanner, name: str, cls):
            registry: ServiceRegistry = getattr(scanner, 'registry')

            # Later we can do some dataclass field sniffing on singletons
            instance = cls()

            # If there is a for_ use it, otherwise, register for the same
            # class as the instance
            for_ = self.for_ if self.for_ else cls
            registry.register_singleton(instance, for_)

        attach(wrapped, callback, category='wired')
        return wrapped


# noinspection PyPep8Naming
class factory:
    def __init__(self, for_=None, context=None, name: str = None):
        self.for_ = for_
        self.context = context if context else for_
        self.name = name

    def __call__(self, wrapped):
        def callback(scanner: Scanner, name: str, cls):
            registry: ServiceRegistry = getattr(scanner, 'registry')
            # If there is a for_ use it, otherwise, register for the same
            # class as the instance
            for_ = self.for_ if self.for_ else cls
            register_dataclass(registry, cls, for_=for_, context=self.context)

        attach(wrapped, callback, category='wired')
        return wrapped
