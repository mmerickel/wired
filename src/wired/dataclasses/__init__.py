"""

TODO

- Convert dataclasses/index.rst samples into files included and tested

- register_singleton and make the simplest test using it

- More tests for context-sensitive, injected, attr, transitive, and others
  from the unit tests

- Decorators

- Request/View/Context/Datastore pattern

- TODO wired-paul.readthedocs.io

- TODO change the dcdi tutorial to not need ``for_`` since the thing being looked up is a subclass

- TODO figure out backport of dataclasses

- TODO for_ allows not inheriting in order to get matches

"""

from .field_types import InjectedArgumentException, injected
from .injector import Injector
from .models import Context

__all__ = [
    InjectedArgumentException,
    injected,
    Injector,
    Context,
]


