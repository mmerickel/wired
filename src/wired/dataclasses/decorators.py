from venusian import attach, Scanner
from wired import ServiceRegistry

from .registration import register_dataclass


# noinspection PyPep8Naming
class singleton:
    """
    Register an instance of a dataclass as a singleton.

    The singleton will be registered with a :class:`wired.ServiceRegistry` when
    performing a venusian scan.

    .. code-block:: python

        @singleton
        @dataclass
        class Settings:
            punctuation: str = ''

    .. seealso:: :meth:`wired.ServiceRegistry.register_singleton`

    """

    def __init__(self, for_=None, context=None, name: str = ''):
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
            registry.register_singleton(
                instance, for_, context=self.context, name=self.name
            )

        attach(wrapped, callback, category='wired')
        return wrapped


# noinspection PyPep8Naming
class factory:
    """
    Register a factory for a dataclass that can sniff dependencies.

    The factory will be registered with a :class:`wired.ServiceRegistry` when
    performing a venusian scan.

    .. code-block:: python

        from sqlalchemy.orm import Session

        @factory
        @dataclass
        class LoginService:
            db: Session

        # ... later

        registry = ServiceRegistry()
        scanner = venusian.Scanner(registry=registry)
        scanner.scan()

        # ... later

        container = registry.create_container()
        svc = container.get(LoginService)

    .. seealso::

        - :func:`wired.dataclasses.register_dataclass`

        - :func:`wired.ServiceRegistry.register_factory`

    """

    def __init__(self, for_=None, context=None, name: str = ''):
        self.for_ = for_
        self.context = context
        self.name = name

    def __call__(self, wrapped):
        def callback(scanner: Scanner, name: str, cls):
            registry: ServiceRegistry = getattr(scanner, 'registry')
            # If there is a for_ use it, otherwise, register for the same
            # class as the instance
            for_ = self.for_ if self.for_ else cls
            register_dataclass(
                registry, cls, for_=for_, context=self.context, name=self.name
            )

        attach(wrapped, callback, category='wired')
        return wrapped
