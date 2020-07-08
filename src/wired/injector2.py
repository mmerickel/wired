"""
Provide arguments to a callable based on wired container.

Functions and dataclasses both take arguments: one as a function signature
and the other as fields.

Use a type-based system to find the needed information for each case, then
call the callable and return it.

TODO
- Provide better error messages to help reduce magic
- Break into smaller, perhaps-replaceable pieces
- Make the injector into a service which can be replaced with
  custom injectors
- Improved typing support
    * The injector function has a return type TypeVar that matches
      what you asked for
"""
from dataclasses import dataclass, field, _FIELDS
from enum import Enum
from inspect import signature, Parameter
from typing import Callable, Optional, Any

from wired import ServiceRegistry, ServiceContainer
from wired.container import Interface


def register_factory(
        registry: ServiceRegistry,
        factory,
        iface_or_type=Interface,
        *,
        context=None,
        name='',
):
    pass


class TargetType(Enum):
    dataclass = 1
    function = 2


@dataclass
class Injector:
    container: ServiceContainer
    target: Callable
    context: Optional[Any] = field(init=False)

    def __post_init__(self):
        self.context = self.container.context

    def _target_type(self):
        """ Determine if the target is a function, dataclass, or other """

        if hasattr(self.target, _FIELDS):
            return TargetType.dataclass
        else:
            return TargetType.function

    def __call__(self):
        args = []
        if self._target_type() is TargetType.function:
            sig = signature(self.target)
            parameters = sig.parameters

            # Pick through the callable's signature and get
            # what is needed.
            for name, param in parameters.items():
                args.append(
                    (
                        name,
                        param.annotation,
                        param.default if param.default is not Parameter.empty else None
                    )
                )

            return args
            return self.target(**kwargs)
