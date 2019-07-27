import pytest


class DummyRegistry:
    for_ = None
    instance = None
    factory = None
    iface_or_type = None
    context = None

    def register_singleton(self, instance, for_):
        self.instance = instance
        self.for_ = for_

    def register_factory(self, factory, iface_or_type, context=None):
        self.factory = factory
        self.iface_or_type = iface_or_type
        self.context = context


class DummyScanner:
    flag = 77

    def __init__(self):
        self.registry = DummyRegistry()


def test_dummy_singleton():
    dr = DummyRegistry()
    dr.register_singleton(99, 88)
    assert 99 == dr.instance
    assert 88 == dr.for_


def test_dummy_factory():
    dr = DummyRegistry()
    dr.register_factory(99, 88, 77)
    assert 99 == dr.factory
    assert 88 == dr.iface_or_type
    assert 77 == dr.context


def test_dummy_scanner():
    ds = DummyScanner()
    assert 77 == ds.flag
    assert isinstance(ds.registry, DummyRegistry)


@pytest.fixture
def dummy_wrapped():
    def wrapped():
        pass

    return wrapped


def test_dummy_wrapped(dummy_wrapped):
    w = dummy_wrapped()
    return None is w


def mockattach(wrapped, callback):
    wrapped.callback = callback


@pytest.fixture
def monkeypatched_dataclasses(monkeypatch, dummy_wrapped):
    # Importing wired.dataclasses imports venusian which then
    # makes it too late to monkeypatch ``venusian.attach``. Centralize
    # the import here where we can do the monkeypatch first.
    monkeypatch.setattr('venusian.attach', mockattach)
    from wired import dataclasses

    return dataclasses


def test_monkeypatched_dataclasses(monkeypatched_dataclasses):
    assert 'wired.dataclasses' == monkeypatched_dataclasses.__name__

    class Wrapped:
        callback: None

    assert None is mockattach(Wrapped(), lambda: None)


def test_singleton_construction_defaults(monkeypatched_dataclasses):
    s = monkeypatched_dataclasses.singleton()
    assert None is s.for_
    assert None is s.context
    assert None is s.name


def test_singleton_construction_for_(monkeypatched_dataclasses):
    s = monkeypatched_dataclasses.singleton(for_=99)
    assert 99 == s.for_
    assert 99 == s.context


def test_singleton_construction_context(monkeypatched_dataclasses):
    s = monkeypatched_dataclasses.singleton(for_=99, context=88)
    assert 99 == s.for_
    assert 88 == s.context


def test_singleton_construction_name(monkeypatched_dataclasses):
    s = monkeypatched_dataclasses.singleton(name='name1')
    assert 'name1' == s.name


def test_factory_construction_defaults(monkeypatched_dataclasses):
    f = monkeypatched_dataclasses.factory()
    assert None is f.for_
    assert None is f.context
    assert None is f.name


def test_factory_construction_for_(monkeypatched_dataclasses):
    f = monkeypatched_dataclasses.factory(for_=99)
    assert 99 == f.for_
    assert 99 == f.context


def test_factory_construction_context(monkeypatched_dataclasses):
    f = monkeypatched_dataclasses.factory(for_=99, context=88)
    assert 99 == f.for_
    assert 88 == f.context


def test_factory_construction_name(monkeypatched_dataclasses):
    f = monkeypatched_dataclasses.factory(name='name1')
    assert 'name1' == f.name
