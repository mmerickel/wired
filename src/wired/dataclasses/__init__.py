"""

TODO

- TODO ``for_`` allows not inheriting in order to get matches

- Unit testing

- register_singleton and make the simplest test using it

- TODO Injection injection (aka transitive injection)

- __call__=True

- TODO Argument sniffing on __call__

- More tests for context-sensitive, injected, attr, transitive, and others
  from the unit tests

- Request/View/Context/Datastore pattern

- TODO Change factory() to factory

- TODO Document @singleton

- TODO Handle InitVar

- TODO Predicates

- TODO Write tests that work with 3.6 and dataclasses backport

"""

from .decorators import factory, singleton
from .field_types import InjectedArgumentException, injected
from .injector import Injector
from .models import Context
from .registration import register_dataclass

__all__ = [
    factory,
    InjectedArgumentException,
    injected,
    Injector,
    Context,
    register_dataclass,
    singleton,
]
