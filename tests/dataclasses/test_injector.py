from dataclasses import dataclass
from typing import Optional

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


class Url:
    pass


@pytest.fixture
def container():
    registry = ServiceRegistry()
    container = registry.create_container()
    return container


def test_service_construction(container):
    inj = Injector(container=container)
    assert container == inj.container


def test_basic_dataclass(monkeypatch, container):
    # Put something in the container

    @dataclass
    class Dummy:
        target: Source

    def d_get(key, context=None):
        return Source()

    monkeypatch.setattr(container, 'get', d_get)
    inj = Injector(container=container)
    result = inj(Dummy)
    assert 'source' == result.target.name


def test_no_registrations(monkeypatch, container):
    # Nothing in registry

    @dataclass
    class Dummy:
        target: Source

    def d_get(key, context=None):
        raise LookupError('Injector failed for target on Dummy')

    monkeypatch.setattr(container, 'get', d_get)
    inj = Injector(container=container)
    with pytest.raises(LookupError) as exc:
        result: Dummy = inj(Dummy)
    assert 'Injector failed for target on Dummy' in str(exc.value)


def test_wrong_registration(monkeypatch, container):
    # Wrong class in registry

    @dataclass
    class Dummy:
        target: WrongSource

    def d_get(key, context=None):
        raise LookupError('Injector failed for target on Dummy')

    monkeypatch.setattr(container, 'get', d_get)
    inj = Injector(container=container)
    with pytest.raises(LookupError) as exc:
        result: Dummy = inj(Dummy)
    assert 'Injector failed for target on Dummy' in str(exc.value)


def test_fail_primitive_value_no_default(monkeypatch, container):
    # Type is str but you don't put primitive values in registry

    @dataclass
    class Dummy:
        target: str

    def d_get(key, context=None):
        if key is Context:
            return Context()
        raise TypeError()

    monkeypatch.setattr(container, 'get', d_get)
    inj = Injector(container=container)
    with pytest.raises(LookupError) as exc:
        result: Dummy = inj(Dummy)
    assert 'No default value on field target' in str(exc.value)


def test_primitive_value_with_default(monkeypatch, container):
    # Type is str but you don't put primitive values in registry

    @dataclass
    class Dummy:
        target: str = 'Dummy Target'

    def d_get(key, context=None):
        if key is Context:
            return Context()
        raise TypeError()

    monkeypatch.setattr(container, 'get', d_get)
    inj = Injector(container=container)
    result: Dummy = inj(Dummy)
    assert 'Dummy Target' == result.target


def test_nothing_needed(monkeypatch, container):
    # Our dataclass doesn't want anything

    @dataclass
    class Dummy:
        pass

    def d_get(key, context=None):
        if key is Context:
            return Context()
        raise TypeError()

    monkeypatch.setattr(container, 'get', d_get)
    inj = Injector(container=container)
    result: Dummy = inj(Dummy)
    assert Dummy == result.__class__


def test_singleton(monkeypatch, container):
    # A singleton is also registered, use it

    @dataclass
    class Dummy:
        target: Source
        singleton: Singleton

    def d_get(key, context=None):
        if key is Context:
            return Context()
        if key is Singleton:
            return Singleton()
        if key is Source:
            return Source()
        raise TypeError()

    monkeypatch.setattr(container, 'get', d_get)
    inj = Injector(container=container)
    result: Dummy = inj(Dummy)
    assert 'source' == result.target.name
    assert 'singleton' == result.singleton.name


def test_container(monkeypatch, container):
    # Target wants to grab the container itself

    @dataclass
    class Dummy:
        container: ServiceContainer

    def d_get(key, context=None):
        if key is Context:
            return Context()
        raise TypeError()

    monkeypatch.setattr(container, 'get', d_get)
    inj = Injector(container=container)
    result: Dummy = inj(Dummy)
    assert container == result.container


def test_container_post_init(monkeypatch, container):
    # Use dataclass post init to get something out of the
    # container

    @dataclass
    class Dummy:
        container: ServiceContainer
        url: Optional[str] = None

        def __post_init__(self):
            self.url = self.container.get(Url)

    def d_get(key, context=None):
        if key is Context:
            return Context()
        if key is Url:
            return Url()
        raise TypeError()

    monkeypatch.setattr(container, 'get', d_get)
    inj = Injector(container=container)
    result: Dummy = inj(Dummy)
    assert container == result.container


def test_injected_field(monkeypatch, container):
    # Using the injected field

    @dataclass
    class Dummy:
        target: Source = injected(Source)

    def d_get(key, context=None):
        if key is Context:
            return Context()
        if key is Source:
            return Source()
        raise TypeError()

    monkeypatch.setattr(container, 'get', d_get)
    inj = Injector(container=container)
    result: Dummy = inj(Dummy)
    assert 'source' == result.target.name


def test_injected_field_with_attr(monkeypatch, container):
    # Using the injected field

    @dataclass
    class Dummy:
        target: str = injected(Source, attr='name')

    def d_get(key, context=None):
        if key is Context:
            return Context()
        if key is Source:
            return Source()
        raise TypeError()

    monkeypatch.setattr(container, 'get', d_get)
    inj = Injector(container=container)
    result: Dummy = inj(Dummy)
    assert 'source' == result.target


def test_injected_field_missing_attr(monkeypatch, container):
    # Using the injected field

    @dataclass
    class Dummy:
        target: str = injected(Source, attr='XXX')

    def d_get(key, context=None):
        if key is Context:
            return Context()
        if key is Source:
            return Source()
        raise TypeError()

    monkeypatch.setattr(container, 'get', d_get)
    inj = Injector(container=container)
    with pytest.raises(AttributeError) as exc:
        result: Dummy = inj(Dummy)
    assert 'XXX' in str(exc.value)
