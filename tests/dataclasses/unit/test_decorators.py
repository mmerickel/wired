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


@pytest.fixture
def dummy_wrapped():
    def wrapped():
        pass

    return wrapped


@pytest.fixture
def monkeypatched_dataclasses(monkeypatch, dummy_wrapped):
    # Importing wired.dataclasses imports venusian which then
    # makes it too late to monkeypatch ``venusian.attach``. Centralize
    # the import here where we can do the monkeypatch first.
    def mockattach(wrapped, callback):
        wrapped.callback = callback

    monkeypatch.setattr('venusian.attach', mockattach)
    from wired import dataclasses
    return dataclasses


def test_singleton_construction_defaults(monkeypatched_dataclasses):
    s = monkeypatched_dataclasses.singleton()
    assert None is s.for_
    assert None is s.context
    assert None is s.name


def test_singleton_construction_for_(monkeypatched_dataclasses):
    s = monkeypatched_dataclasses.singleton(for_=99)
    assert 99 is s.for_
    assert 99 is s.context


def test_singleton_construction_context(monkeypatched_dataclasses):
    s = monkeypatched_dataclasses.singleton(for_=99, context=88)
    assert 99 is s.for_
    assert 88 is s.context


def test_singleton_construction_name(monkeypatched_dataclasses):
    s = monkeypatched_dataclasses.singleton(name='name1')
    assert 'name1' is s.name


# def test_singleton_call(monkeypatched_dataclasses, dummy_wrapped):
#     scanner = DummyScanner()
#     s = monkeypatched_dataclasses.singleton()
#     w = s(dummy_wrapped)
#     callback = w.callback
#     callback(scanner, None, DummyScanner)
#     assert 77 == scanner.registry.instance.flag


def test_factory_construction_defaults(monkeypatched_dataclasses):
    f = monkeypatched_dataclasses.factory()
    assert None is f.for_
    assert None is f.context
    assert None is f.name


def test_factory_construction_for_(monkeypatched_dataclasses):
    f = monkeypatched_dataclasses.factory(for_=99)
    assert 99 is f.for_
    assert 99 is f.context


def test_factory_construction_context(monkeypatched_dataclasses):
    f = monkeypatched_dataclasses.factory(for_=99, context=88)
    assert 99 is f.for_
    assert 88 is f.context


def test_factory_construction_name(monkeypatched_dataclasses):
    f = monkeypatched_dataclasses.factory(name='name1')
    assert 'name1' is f.name


# def test_factory_call(monkeypatched_dataclasses, dummy_wrapped):
#     scanner = DummyScanner()
#     f = monkeypatched_dataclasses.factory()
#     w = f(dummy_wrapped)
#     callback = w.callback
#     callback(scanner, None, DummyScanner)
#     assert 'dataclass_factory' == scanner.registry.factory.__name__
