from dataclasses import dataclass, field
from typing import Optional

import pytest

from wired import ServiceRegistry, ServiceContainer
from wired.dataclasses import injected, Context
from wired.dataclasses.injector import Injector


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


@dataclass
class DummyBasicDataclass:
    target: Source

    # Use this to bundle the monkeypatch
    @staticmethod
    def d_get(key):
        return Source()


def test_dummy_basic_dataclass():
    d = DummyBasicDataclass(target=Source())
    assert isinstance(d.target, Source)
    d1 = DummyBasicDataclass.d_get(Source)
    assert isinstance(d1, Source)


def test_basic_dataclass(monkeypatch, container):
    # Put something in the container

    monkeypatch.setattr(container, 'get', DummyBasicDataclass.d_get)
    inj = Injector(DummyBasicDataclass)
    result = inj(container)
    assert 'source' == result.target.name


@dataclass
class DummyNoRegistrations:
    target: Source

    # Use this to bundle the monkeypatch
    @staticmethod
    def d_get(key):
        raise LookupError('Injector failed for target on DummyNoRegistrations')


def test_dummy_no_registrations():
    d = DummyNoRegistrations(target=Source())
    assert isinstance(d.target, Source)
    with pytest.raises(LookupError):
        DummyNoRegistrations.d_get(Source)


def test_no_registrations(monkeypatch, container):
    # Nothing in registry

    monkeypatch.setattr(container, 'get', DummyNoRegistrations.d_get)
    inj = Injector(DummyNoRegistrations)
    with pytest.raises(LookupError) as exc:
        inj(container)
    msg = 'Injector failed for target on DummyNoRegistrations'
    assert msg == str(exc.value)


@dataclass
class DummyWrongRegistrations:
    target: WrongSource

    # Use this to bundle the monkeypatch
    @staticmethod
    def d_get(key):
        msg = 'Injector failed for target on DummyWrongRegistrations'
        raise LookupError(msg)


def test_dummy_wrong_registrations():
    d = DummyWrongRegistrations(target=WrongSource())
    assert isinstance(d.target, WrongSource)
    with pytest.raises(LookupError):
        DummyWrongRegistrations.d_get(Source)


def test_wrong_registration(monkeypatch, container):
    # Wrong class in registry

    monkeypatch.setattr(container, 'get', DummyWrongRegistrations.d_get)
    inj = Injector(DummyWrongRegistrations)
    with pytest.raises(LookupError) as exc:
        inj(container)
    msg = 'Injector failed for target on DummyWrongRegistrations'
    assert msg == str(exc.value)


@dataclass
class DummyFailPVND:
    target: str

    # Use this to bundle the monkeypatch
    @staticmethod
    def d_get(key):
        raise TypeError()


def test_dummy_fail_pvnd():
    d = DummyFailPVND(target='dummypvnd')
    assert isinstance(d.target, str)
    with pytest.raises(TypeError):
        DummyFailPVND.d_get(Source)


def test_fail_primitive_value_no_default(monkeypatch, container):
    # Type is str but you don't put primitive values in registry

    monkeypatch.setattr(container, 'get', DummyFailPVND.d_get)
    inj = Injector(DummyFailPVND)
    with pytest.raises(LookupError) as exc:
        inj(container)
    msg = 'No default value on field target'
    assert msg == str(exc.value)


def test_primitive_value_with_default(container):
    # Type is str but you don't put primitive values in registry

    @dataclass
    class Dummy:
        target: str = 'Dummy Target'

    inj = Injector(Dummy)
    result: Dummy = inj(container)
    assert 'Dummy Target' == result.target


def test_nothing_needed(container):
    # Our dataclass doesn't want anything

    @dataclass
    class Dummy:
        pass

    inj = Injector(Dummy)
    result: Dummy = inj(container)
    assert Dummy == result.__class__


@dataclass
class DummySingleton:
    singleton: Singleton

    # Use this to bundle the monkeypatch
    @staticmethod
    def d_get(key) -> Singleton:
        if key is Singleton:
            return Singleton()
        raise TypeError()


def test_dummy_singleton():
    ds = DummySingleton(singleton=Singleton())
    d1 = DummySingleton.d_get(Singleton)
    assert isinstance(d1, Singleton)
    with pytest.raises(TypeError):
        ds.d_get(None)


def test_singleton(monkeypatch, container):
    # A singleton is also registered, use it

    monkeypatch.setattr(container, 'get', DummySingleton.d_get)
    inj = Injector(DummySingleton)
    result: DummySingleton = inj(container)
    assert 'singleton' == result.singleton.name


@dataclass
class DummyContainer:
    container: ServiceContainer


def test_dummy_container():
    sc = ServiceContainer(factories=[])
    dc = DummyContainer(container=sc)
    assert isinstance(dc.container, ServiceContainer)


def test_container(container):
    # Target wants to grab the container itself

    inj = Injector(DummyContainer)
    result: DummyContainer = inj(container)
    assert container == result.container


@dataclass
class DummyInit:
    container: ServiceContainer
    name: str = field(init=False)

    def __post_init__(self):
        self.name = 'initialized'


def test_dummy_init():
    di = DummyInit(ServiceContainer(factories=[]))
    assert isinstance(di.container, ServiceContainer)
    assert 'initialized' == di.name


def test_init_false(container):
    # Use __post_init__ to initialize a field

    inj = Injector(DummyInit)
    result: DummyInit = inj(container)
    assert 'initialized' == result.name


@dataclass
class DummyNotInit:
    container: ServiceContainer
    name: str = field(init=False)


def test_init_false_missing_postinit(container):
    # A field has init=False but the dataclass is missing a __post_init__

    inj = Injector(DummyNotInit)
    with pytest.raises(LookupError) as exc:
        inj(container)
    expected = 'Field "name" has init=False but no __post_init__'
    assert expected == str(exc.value)


@dataclass
class DummyInjected:
    context: Context


def test_dummy_injected():
    context = Context()
    di = DummyInjected(context=context)
    assert context == di.context


def test_injected_context(container, dummy_customer):
    # Return the context from the container.context via injection

    container.context = dummy_customer
    inj = Injector(DummyInjected)
    result: DummyInjected = inj(container)
    assert 'dummy_customer' == getattr(result.context, 'name')


def test_injected_customer_from_container_attr(container, dummy_customer):
    # Slightly-better spelling for getting context, but as correct type

    @dataclass
    class Dummy:
        context: DummyCustomer = injected(ServiceContainer, attr='context')

    container.context = dummy_customer
    inj = Injector(Dummy)
    result: Dummy = inj(container)
    assert 'dummy_customer' == getattr(result.context, 'name')


def test_injected_customer_from_injector(container, dummy_customer):
    # The best spelling for getting the context as the correct type

    @dataclass
    class Dummy:
        context: DummyCustomer = injected(Context)

    container.context = dummy_customer
    inj = Injector(Dummy)
    result: Dummy = inj(container)
    assert 'dummy_customer' == getattr(result.context, 'name')


def test_no_registered_or_manual_context(container):
    # No context assigned to container
    @dataclass
    class Dummy:
        context: Context

    inj = Injector(Dummy)
    result: Dummy = inj(container)
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

    def d_get(key):
        if key is Url:
            return Url()
        raise TypeError()

    monkeypatch.setattr(container, 'get', d_get)
    container.context = dummy_customer
    inj = Injector(Dummy)
    result: Dummy = inj(container)
    assert container == result.container


@dataclass
class DummyInjectedField:
    target: Source = injected(Source)

    # Use this to bundle the monkeypatch
    @staticmethod
    def d_get(key, name=''):
        return Source()


def test_dummy_injected_field():
    d = DummyInjectedField(target=Source())
    assert isinstance(d.target, Source)
    d1 = DummyInjectedField.d_get(Source)
    assert isinstance(d1, Source)


def test_injected_field(monkeypatch, container):
    # Using the injected field

    monkeypatch.setattr(container, 'get', DummyInjectedField.d_get)
    inj = Injector(DummyInjectedField)
    result: DummyInjectedField = inj(container)
    assert 'source' == result.target.name


@dataclass
class DummyInjectedSingleton:
    target: Source = injected(Source)

    # Use this to bundle the monkeypatch
    @staticmethod
    def d_get(key, name=''):
        return Source()


def test_dummy_injected_singleton():
    d = DummyInjectedSingleton(target=Source())
    assert isinstance(d.target, Source)
    d1 = DummyInjectedSingleton.d_get(Source)
    assert isinstance(d1, Source)


def test_injected_singleton(monkeypatch, container):
    # Using the injected field to find a singleton

    monkeypatch.setattr(container, 'get', DummyInjectedSingleton.d_get)
    inj = Injector(DummyInjectedSingleton)
    result: DummyInjectedSingleton = inj(container)
    assert 'source' == result.target.name


@dataclass
class DummyIFWA:
    target: str = injected(Source, attr='name')

    # Use this to bundle the monkeypatch
    @staticmethod
    def d_get(key, name=''):
        return Source()


def test_dummy_ifwa():
    d = DummyIFWA(target='target')
    assert isinstance(d.target, str)
    d1 = DummyIFWA.d_get(Source)
    assert isinstance(d1, Source)


def test_injected_field_with_attr(monkeypatch, container):
    # Using the injected field

    monkeypatch.setattr(container, 'get', DummyIFWA.d_get)
    inj = Injector(DummyIFWA)
    result: DummyIFWA = inj(container)
    assert 'source' == result.target


@dataclass
class DummyIFMA:
    target: str = injected(Source, attr='XXX')

    # Use this to bundle the monkeypatch
    @staticmethod
    def d_get(key, name=''):
        if key is Source:
            return Source()
        raise TypeError()


def test_dummy_ifma():
    d = DummyIFMA(target='dummy')
    assert isinstance(d.target, str)
    d1 = DummyIFMA.d_get(Source)
    assert isinstance(d1, Source)
    with pytest.raises(TypeError):
        DummyIFMA.d_get(Singleton)


def test_injected_field_missing_attr(monkeypatch, container):
    # Using the injected field

    monkeypatch.setattr(container, 'get', DummyIFMA.d_get)
    inj = Injector(DummyIFMA)
    with pytest.raises(AttributeError) as exc:
        inj(container)
    assert 'XXX' in str(exc.value)
