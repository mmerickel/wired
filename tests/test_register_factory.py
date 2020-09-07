"""
Refactor register_factory to streamline registrations with closures.

https://github.com/mmerickel/wired/issues/35
"""

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


def test_decorator_args():
    """ Call the decorator with context etc. """
    from .factories import decorator_args
    from .factories.decorator_args import LoginService, CustomLoginService
    registry = ServiceRegistry()

    # First register the "built-in" service, then scan to get
    # the custom override
    registry.register_service(LoginService)
    scanner = Scanner(registry=registry)
    scanner.scan(decorator_args)

    # Container and lookup for custom service
    container: ServiceContainer = registry.create_container()
    result: CustomLoginService = container.get(LoginService)
    assert isinstance(result, CustomLoginService)


def test_decorator_context():
    """ Two decorators each with a registered context """
    from .factories import decorator_context
    from .factories.decorator_context import (
        LoginService, CustomLoginService,
        Customer, CustomCustomer,
    )
    registry = ServiceRegistry()

    # First register the "built-in" service, then scan to get
    # the custom override
    scanner = Scanner(registry=registry)
    scanner.scan(decorator_context)

    # Container and lookup for context=Customer
    context1 = Customer()
    container1: ServiceContainer = registry.create_container(context=context1)
    result1: CustomLoginService = container1.get(LoginService)
    assert isinstance(result1, LoginService)

    # Container and lookup for context=CustomCustomer
    context2 = CustomCustomer()
    container2: ServiceContainer = registry.create_container(context=context2)
    result2: CustomLoginService = container2.get(LoginService)
    assert isinstance(result2, CustomLoginService)


def test_custom_constructor_imperative():
    """ Service has a ``__wired_factory__ classmethod """
    from .factories import custom_factory
    from .factories.custom_factory import registry, LoginService
    scanner = Scanner(registry=registry)
    scanner.scan(custom_factory)

    # Look up the login service
    container: ServiceContainer = registry.create_container()
    result: LoginService = container.get(LoginService)
    assert 'Some Customer' == result.customer_name


def test_custom_constructor_decorator():
    """ Service has a ``__wired_factory__ classmethod and decorator """
    from .factories import custom_factory_decorator
    from .factories.custom_factory_decorator import LoginService
    registry = ServiceRegistry()
    scanner = Scanner(registry=registry)
    scanner.scan(custom_factory_decorator)

    # Look up the login service
    container: ServiceContainer = registry.create_container()
    result: LoginService = container.get(LoginService)
    assert 'Some Customer' == result.customer_name
