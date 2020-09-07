"""
Refactor register_factory to streamline registrations with closures.

https://github.com/mmerickel/wired/issues/35
"""
import pytest

from wired import ServiceContainer, ServiceRegistry

try:
    from venusian import attach, Scanner
except ImportError:
    attach = None
    Scanner = None


def test_current():
    """ Current, pre-refactor behavior """
    from .factories.current import registry, LoginService
    container: ServiceContainer = registry.create_container()
    result: LoginService = container.get(LoginService)
    assert isinstance(result, LoginService)


def test_autogenerate():
    """ Simplest case, just generate a closure as factory function """
    from .factories.autofunction import registry, LoginService
    container: ServiceContainer = registry.create_container()
    result: LoginService = container.get(LoginService)
    assert isinstance(result, LoginService)


def test_autogenerate_no_interface():
    """ Same but fails if using an interface instead of a class """
    from .factories.autofunction_interface import registry, ILogin
    container: ServiceContainer = registry.create_container()
    with pytest.raises(ValueError) as exc:
        container.get(ILogin)
    assert 'ILogin is not a class' == str(exc.value)


def test_first_decorator():
    """ Same as autogenerate but with decorator """
    from .factories import first_decorator
    from .factories.first_decorator import LoginService
    registry = ServiceRegistry()
    scanner = Scanner(registry=registry)
    scanner.scan(first_decorator)
    container: ServiceContainer = registry.create_container()
    result: LoginService = container.get(LoginService)
    assert isinstance(result, LoginService)
