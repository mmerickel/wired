from dataclasses import dataclass, field
from typing import Optional

import pytest

from wired import ServiceRegistry, ServiceContainer
from wired.dataclasses import injected, Injector, Context


class Source:
    name = 'source'


class WrongSource:
    name = 'wrongsource'


class Singleton:
    name = 'singleton'


class Url:
    pass


@dataclass
class DummyCustomer:
    """ Use this as a context in the container """
    name: str = 'dummy_customer'


@pytest.fixture
def dummy_customer():
    return DummyCustomer()


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

    def d_get(key):
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

    def d_get(key):
        raise LookupError('Injector failed for target on Dummy')

    monkeypatch.setattr(container, 'get', d_get)
    inj = Injector(container=container)
    with pytest.raises(LookupError) as exc:
        inj(Dummy)
    assert 'Injector failed for target on Dummy' in str(exc.value)


def test_wrong_registration(monkeypatch, container):
    # Wrong class in registry

    @dataclass
    class Dummy:
        target: WrongSource

    def d_get(key):
        raise LookupError('Injector failed for target on Dummy')

    monkeypatch.setattr(container, 'get', d_get)
    inj = Injector(container=container)
    with pytest.raises(LookupError) as exc:
        inj(Dummy)
    assert 'Injector failed for target on Dummy' in str(exc.value)


def test_fail_primitive_value_no_default(monkeypatch, container):
    # Type is str but you don't put primitive values in registry

    @dataclass
    class Dummy:
        target: str

    def d_get(key):
        raise TypeError()

    monkeypatch.setattr(container, 'get', d_get)
    inj = Injector(container=container)
    with pytest.raises(LookupError) as exc:
        Dummy = inj(Dummy)
    assert 'No default value on field target' in str(exc.value)


def test_primitive_value_with_default(container):
    # Type is str but you don't put primitive values in registry

    @dataclass
    class Dummy:
        target: str = 'Dummy Target'

    inj = Injector(container=container)
    result: Dummy = inj(Dummy)
    assert 'Dummy Target' == result.target


def test_nothing_needed(container):
    # Our dataclass doesn't want anything

    @dataclass
    class Dummy:
        pass

    inj = Injector(container=container)
    result: Dummy = inj(Dummy)
    assert Dummy == result.__class__


def test_singleton(monkeypatch, container):
    # A singleton is also registered, use it

    @dataclass
    class Dummy:
        target: Source
        singleton: Singleton

    def d_get(key):
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


def test_container(container):
    # Target wants to grab the container itself

    @dataclass
    class Dummy:
        container: ServiceContainer

    inj = Injector(container=container)
    result: Dummy = inj(Dummy)
    assert container == result.container


def test_init_false(container):
    # Use __post_init__ to initialize a field

    @dataclass
    class Dummy:
        container: ServiceContainer
        name: str = field(init=False)

        def __post_init__(self):
            self.name = 'initialized'

    inj = Injector(container=container)
    result: Dummy = inj(Dummy)
    assert 'initialized' == result.name


def test_init_false_missing_postinit(container):
    # A field has init=False but the dataclass is missing a __post_init__

    @dataclass
    class Dummy:
        container: ServiceContainer
        name: str = field(init=False)

        def __XXX_INIT__(self):
            self.name = 'notinitialized'

    inj = Injector(container=container)
    with pytest.raises(LookupError) as exc:
        Dummy = inj(Dummy)
    expected = 'Field "name" has init=False but no __post_init__'
    assert expected == str(exc.value)


def test_injected_context(container, dummy_customer):
    # Return the context from the container.context via injection

    @dataclass
    class Dummy:
        context: Context

    container.context = dummy_customer
    inj = Injector(container=container)
    result: Dummy = inj(Dummy)
    assert 'dummy_customer' == getattr(result.context, 'name')


def test_injected_customer_from_container_attr(container, dummy_customer):
    # Slightly-better spelling for getting context, but as correct type

    @dataclass
    class Dummy:
        context: DummyCustomer = injected(ServiceContainer, attr='context')

    container.context = dummy_customer
    inj = Injector(container=container)
    result: Dummy = inj(Dummy)
    assert 'dummy_customer' == getattr(result.context, 'name')


def test_injected_customer_from_injector(container, dummy_customer):
    # The best spelling for getting the context as the correct type

    @dataclass
    class Dummy:
        context: DummyCustomer = injected(Context)

    container.context = dummy_customer
    inj = Injector(container=container)
    result: Dummy = inj(Dummy)
    assert 'dummy_customer' == getattr(result.context, 'name')


def test_no_registered_or_manual_context(container):
    # No context assigned to container
    @dataclass
    class Dummy:
        context: Context

    inj = Injector(container=container)
    result: Dummy = inj(Dummy)
    assert None is result.context


def test_container_post_init(monkeypatch, container, dummy_customer):
    # Use dataclass post init to get something out of the
    # container

    @dataclass
    class Dummy:
        container: ServiceContainer
        url: Optional[str] = None

        def __post_init__(self):
            self.url = self.container.get(Url)

    def d_get(key, context=None):
        if key is Url:
            return Url()
        raise TypeError()

    monkeypatch.setattr(container, 'get', d_get)
    container.context = dummy_customer
    inj = Injector(container=container)
    result: Dummy = inj(Dummy)
    assert container == result.container


def test_injected_field(monkeypatch, container):
    # Using the injected field

    @dataclass
    class Dummy:
        target: Source = injected(Source)

    def d_get(key):
        if key is Source:
            return Source()
        raise TypeError()

    monkeypatch.setattr(container, 'get', d_get)
    inj = Injector(container=container)
    result: Dummy = inj(Dummy)
    assert 'source' == result.target.name


def test_injected_singleton(monkeypatch, container):
    # Using the injected field to find a singleton

    @dataclass
    class Dummy:
        target: Source = injected(Source)

    def d_get(key):
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

    def d_get(key):
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

    def d_get(key):
        if key is Source:
            return Source()
        raise TypeError()

    monkeypatch.setattr(container, 'get', d_get)
    inj = Injector(container=container)
    with pytest.raises(AttributeError) as exc:
        Dummy = inj(Dummy)
    assert 'XXX' in str(exc.value)
