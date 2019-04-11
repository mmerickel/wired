from dataclasses import dataclass

import pytest
from wired import ServiceRegistry, ServiceContainer
from wired.dataclasses.field_types import injected
from wired.dataclasses.injector import Injector, Context


class Source:
    name = 'source'


class WrongSource:
    name = 'wrongsource'


class Singleton:
    name = 'singleton'


@pytest.fixture
def empty_container(monkeypatch):
    registry = ServiceRegistry()
    d = {
        Context: Context(),
    }

    def d_get(key):
        if key not in d:
            raise LookupError()
        return d.get(key)

    container = registry.create_container()
    monkeypatch.setattr(container, 'get', d_get)
    return container


@pytest.fixture
def container(monkeypatch):
    registry = ServiceRegistry()
    d = {
        Context: Context(),
        Source: Source(),
        Singleton: Singleton(),
    }

    def d_get(key, context=None):
        if key not in d:
            raise LookupError()
        return d.get(key)

    container = registry.create_container()
    monkeypatch.setattr(container, 'get', d_get)
    return container


def test_service_construction(container):
    injector = Injector(container=container)
    assert container == injector.container


def test_basic_dataclass(container):
    # Put something in the container

    @dataclass
    class Dummy:
        target: Source

    injector = Injector(container=container)
    result = injector(Dummy)
    assert 'source' == result.target.name


def test_no_registrations(empty_container):
    # Nothing in registry

    @dataclass
    class Dummy:
        target: Source

    injector = Injector(container=empty_container)
    result: Dummy = injector(Dummy)
    assert 9 == result


def test_wrong_registration(container):
    # Wrong class in registry

    @dataclass
    class Dummy:
        target: WrongSource

    injector = Injector(container=container)
    with pytest.raises(TypeError) as exc:
        result: Dummy = injector(Dummy)
    assert 'missing 1 required positional argument' in str(exc.value)


def test_nothing_needed(empty_container):
    # Our dataclass doesn't want anything

    @dataclass
    class Dummy:
        pass

    injector = Injector(container=empty_container)
    result: Dummy = injector(Dummy)
    assert Dummy == result.__class__


def test_singleton(container):
    # A singleton is also registered, use it

    @dataclass
    class Dummy:
        target: Source
        singleton: Singleton

    injector = Injector(container=container)
    result: Dummy = injector(Dummy)
    assert 'source' == result.target.name
    assert 'singleton' == result.singleton.name


def test_container(container):
    # Target wants to grab the container itself

    @dataclass
    class Dummy:
        container: ServiceContainer

    injector = Injector(container=container)
    result: Dummy = injector(Dummy)
    assert container == result.container


def test_injected_field(container):
    # Using the injected field

    @dataclass
    class Dummy:
        target: Source = injected(Source)

    injector = Injector(container=container)
    result: Dummy = injector(Dummy)
    assert 'source' == result.target.name


def test_injected_field_with_attr(container):
    # Using the injected field

    @dataclass
    class Dummy:
        target: str = injected(Source, attr='name')

    injector = Injector(container=container)
    result: Dummy = injector(Dummy)
    assert 'source' == result.target


def test_injected_field_missing_attr(container):
    # Using the injected field

    @dataclass
    class Dummy:
        target: str = injected(Source, attr='XXX')

    injector = Injector(container=container)
    with pytest.raises(AttributeError) as exc:
        result: Dummy = injector(Dummy)
    assert 'XXX' in str(exc.value)
