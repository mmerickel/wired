import pytest

from examples.decorators import (
    basic_class,
    decorator_args,
    decorator_with_wired_factory,
    no_decorator,
    no_decorator_class,
)
from examples.wired_factory import register_wired_factory


@pytest.mark.parametrize(
    'target',
    (
        no_decorator,
        no_decorator_class,
        basic_class,
        decorator_with_wired_factory,
        register_wired_factory,
        decorator_args,
    ),
)
def test_greeter(target):
    target.app()
