import pytest

from examples.decorators import (
    no_decorator,
    no_decorator_class,
    basic_class,
    decorator_with_wired_factory,
)


@pytest.mark.parametrize(
    'target',
    (
            no_decorator,
            no_decorator_class,
            basic_class,
            decorator_with_wired_factory,
    ),
)
def test_greeter(target):
    target.app()
