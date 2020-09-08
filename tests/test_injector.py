from dataclasses import dataclass

import pytest

from wired import ServiceRegistry, ServiceContainer
from wired.injector import Injector, _target_type, TargetType, Injected


@pytest.fixture
def this_container() -> ServiceContainer:
    r = ServiceRegistry()
    c = r.create_container()
    return c


@pytest.fixture
def this_injector(this_container) -> Injector:
    return Injector(container=this_container)


class DummyService:
    """ Some marker """
    pass


def test_target_type():
    @dataclass
    class Target:
        pass

    def target():
        return

    assert TargetType.function == _target_type(target)
    assert TargetType.dataclass == _target_type(Target)


def test_handle_field_none(this_injector):
    class Unknown:
        pass

    assert None is this_injector(Unknown)


def test_handle_field_container(this_injector):
    # E.g. (c: ServiceContainer)
    field_type = this_injector.handle_field(ServiceContainer)
    assert ServiceContainer is field_type.__class__


def test_function_no_args(this_injector):
    """ The callable has no arguments """

    def dummy_service():
        return 99

    result = this_injector(target=dummy_service)
    assert 99 == result


def test_container_by_name(this_injector):
    """ The callable wants the container, but doesn't use type hints """

    def dummy_service(container):
        return 99

    result = this_injector(target=dummy_service)
    assert 99 == result


def test_container_by_type(this_injector):
    """ The callable wants the container, not by name, but type """

    def dummy_service(c: ServiceContainer):
        return 99

    result = this_injector(target=dummy_service)
    assert 99 == result


def test_handle_field_injected_servicecontainer(this_injector):
    def dummy_service(c: Injected[ServiceContainer]):
        return 99

    result = this_injector(target=dummy_service)
    assert 99 == result


def test_handle_field_injected_customer(this_container, this_injector):
    class Customer:
        pass

    this_container.register_singleton(Customer(), Customer)

    def dummy_service(customer: Injected[Customer]):
        return customer

    result = this_injector(target=dummy_service)
    assert Customer is result.__class__
