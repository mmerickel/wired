from dataclasses import dataclass

import pytest

from wired import ServiceRegistry, ServiceContainer
from wired.injector2 import Injector, _target_type, TargetType


@pytest.fixture
def this_container() -> ServiceContainer:
    r = ServiceRegistry()
    c = r.create_container()
    return ServiceContainer


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


def test_function_no_args(this_container):
    """ The callable has no arguments """

    def dummy_service():
        return 99

    injector = Injector(container=this_container)
    result = injector(target=dummy_service)
    assert 99 == result


def test_container_by_name():
    """ The callable wants the container, but doesn't use type hints """

    def dummy_service(container):
        return 99

    injector = Injector(container=this_container)
    result = injector(target=dummy_service)
    assert 99 == result


def test_container_by_type():
    """ The callable wants the container, not by name, but type """

    def dummy_service(c: ServiceContainer):
        return 99

    injector = Injector(container=this_container)
    result = injector(target=dummy_service)
    assert 99 == result
