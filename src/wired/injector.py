"""
Provide arguments to a callable based on wired container.

Functions and dataclasses both take arguments: one as a function signature
and the other as fields.

Use a type-based system to find the needed information for each case, then
call the callable and return it.

TODO
- Make the injector into a service which can be replaced with
  custom injectors
- Provide better error messages to help reduce magic
- Break into smaller, perhaps-replaceable pieces
- Improved typing support
"""

from dataclasses import dataclass, field, _FIELDS
from enum import Enum
from inspect import signature, isfunction
from typing import Optional, Any, TypeVar, Type, Union, Callable, get_args

from wired import ServiceContainer

# TODO Decide on how to express the optional requirement on typing
#    for < Python 3.9 ... could use the technique from
#    https://github.com/alecthomas/injector/blob/master/injector/__init__.py

try:
    from typing import Annotated
    from typing import get_type_hints
except ImportError:
    # Need the updated get_type_hints which allows include_extras=True
    from typing_extensions import Annotated, get_type_hints

_inject_marker = object()
InjectT = TypeVar('InjectT')
Injected = Annotated[InjectT, _inject_marker]


class TargetType(Enum):
    dataclass = 1
    function = 2


T = TypeVar('T')


def _target_type(target: Union[Type[T], Callable]):
    """ Determine if the target is a function, dataclass, or other """

    if hasattr(target, _FIELDS):
        return TargetType.dataclass
    elif isfunction(target):
        return TargetType.function


@dataclass
class Injector:
    container: ServiceContainer
    context: Optional[Any] = field(init=False)

    def __post_init__(self):
        self.context = getattr(self.container, 'context', None)

    def handle_field(self, _type_hint):
        # Special case: Asking for ServiceContainer doesn't need
        # a trip to the container.
        if _type_hint is ServiceContainer:
            return self.container

        # We're using Annotated[]
        if _inject_marker in _type_hint.__metadata__:
            a_type, *modifiers = get_args(_type_hint)
            if a_type is ServiceContainer:
                # Don't go to the container to look up the container
                return self.container

            factory_result = self.container.get(a_type)
            return factory_result

    def handle_function(self, target: Callable):
        """ Call a function using dependency injection """
        args = []
        sig = signature(target)
        parameters = sig.parameters
        type_hints = get_type_hints(target, include_extras=True)

        # Pick through callable's signature and get what's needed.
        param_values = parameters.values()
        if len(param_values) == 1 and \
                list(param_values)[0].name == 'container':
            # Special case for default, original wired behavior:
            # if the callable wants the container, and there's one
            # parameter, and it has a name of container...use it.
            return target(self.container)

        for index, param in enumerate(parameters.values()):
            param_type = type_hints[param.name]

            # Special case: Asking for ServiceContainer doesn't need
            # a trip to the container.
            args.append(self.handle_field(param_type))

        return target(*args)

    def __call__(self, target: Union[Type[T], Callable]) -> T:
        target_type = _target_type(target)
        if target_type is TargetType.function:
            return self.handle_function(target)


"""
Previous
for name, param in parameters.items():
    args.append(
        (
            name,
            param.annotation,
            param.default if param.default is not empty else None
        )
    )
"""
