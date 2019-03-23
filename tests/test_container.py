import pytest
from zope.interface import Interface
from zope.interface import implementer


class IFooService(Interface):
    pass


class IBarService(IFooService):
    pass


class IBazService(IFooService):
    pass


class ContextA:
    pass


class IContextInterface(Interface):
    pass


@implementer(IContextInterface)
class ContextWithInterface:
    pass


class DummyService:
    pass


class DummyFactory:
    def __init__(self, result=None):
        if result is None:
            result = DummyService()
        self.result = result
        self.calls = []

    def __call__(self, container):
        self.calls.append(container)
        return self.result


@pytest.fixture
def registry():
    from wired import ServiceRegistry

    return ServiceRegistry()


def test_sentinel_repr():
    from wired.container import _marker

    assert str(_marker) == '<default>'


@pytest.mark.parametrize('iface', [Interface, IFooService, DummyService])
@pytest.mark.parametrize('name', ['', 'foo'])
@pytest.mark.parametrize(
    'contexts',
    [
        (None, None),
        (None, ContextA()),  # fallback to None lookup
        (ContextA, ContextA()),
        (IContextInterface, ContextWithInterface()),
        pytest.param((IContextInterface, ContextA()), marks=pytest.mark.xfail),
    ],
)
def test_various_params(registry, iface, contexts, name):
    context_iface, context_obj = contexts
    factory = DummyFactory()
    registry.register_factory(factory, iface, context=context_iface, name=name)
    c = registry.create_container()
    assert c.get(iface, context=context_obj, name=name) is factory.result
    assert c.get(iface, context=context_obj, name=name) is factory.result
    assert len(factory.calls) == 1


def test_basic_caching(registry):
    factory = DummyFactory()
    registry.register_factory(factory, name='foo')
    c1 = registry.create_container()
    assert c1.get(name='foo') is factory.result
    assert c1.get(name='foo') is factory.result
    c2 = c1.bind(context=ContextA())
    assert c2.get(name='foo') is factory.result
    assert len(factory.calls) == 1


def test_basic_singletons(registry):
    svc = DummyService()
    registry.register_singleton(svc, name='foo')
    c1 = registry.create_container()
    assert c1.get(name='foo') is svc
    c2 = registry.create_container()
    assert c2.get(name='foo') is svc


def test_bind_context(registry):
    factory = DummyFactory()
    registry.register_factory(factory, name='foo')
    ctx = object()
    c1 = registry.create_container()
    c2 = c1.bind(context=ctx)
    assert c1.cache is c2.cache
    assert c1.factories is c2.factories
    c3 = c2.bind(context=ctx)
    assert c2 is c3


def test_different_contexts_in_nested_lookup(registry):
    class UserRoles:
        pass

    class AdminRoles(UserRoles):
        pass

    class DefaultRoles(UserRoles):
        pass

    class User:
        def __init__(self, roles):
            self.roles = roles

    class AdminArea:
        pass

    class DefaultArea:
        pass

    def admin_roles_factory(_):
        return AdminRoles()

    registry.register_factory(
        admin_roles_factory, UserRoles, context=AdminArea
    )

    def default_roles_factory(_):
        return DefaultRoles()

    registry.register_factory(
        default_roles_factory, UserRoles, context=DefaultArea
    )

    def user_factory(container):
        roles = container.get(UserRoles)
        return User(roles)

    registry.register_factory(user_factory, User, context=Interface)

    c = registry.create_container()
    user1 = c.get(User, context=AdminArea())
    assert isinstance(user1.roles, AdminRoles)
    user2 = c.get(User, context=DefaultArea())
    assert user1 is not user2
    assert isinstance(user2.roles, DefaultRoles)
    with pytest.raises(LookupError):
        # no context defined so cannot find appropriate roles
        c.get(User)


def test_override_cache_via_set(registry):
    db = DummyService()
    db_factory = DummyFactory()
    registry.register_factory(db_factory, name='db')
    c = registry.create_container()
    c.set(db, context=ContextA, name='db')
    assert c.get(name='db') is db_factory.result
    assert c.get(name='db', context=ContextA()) is db


def test_override_cache_via_set_fails(registry):
    db = DummyService()
    db_factory = DummyFactory()
    registry.register_factory(db_factory, name='db')
    c = registry.create_container()
    assert c.get(name='db') is db_factory.result
    with pytest.raises(ValueError):
        c.set(db, context=ContextA, name='db')


def test_find_factory(registry):
    factory = DummyFactory()
    registry.register_factory(factory, name='foo')
    assert registry.find_factory(name='foo') is factory


def test_unregistered_factory_lookup(registry):
    assert registry.find_factory(name='foo') is None
    assert registry.find_factory(IFooService) is None


def test_unregistered_lookup(registry):
    marker = object()
    factory = DummyFactory()
    registry.register_factory(factory, name='bar')
    registry.register_factory(factory, IFooService)
    c = registry.create_container()
    with pytest.raises(LookupError):
        c.get(name='foo')
    with pytest.raises(LookupError):
        c.get(IBarService)  # IFooService is not specific enough
    assert c.get(IBarService, default=marker) is marker


def test_unique_class_objects_with_same_name_dont_conflict(registry):
    def make_class():
        class Greeter:
            pass

        return Greeter

    ClassA = make_class()
    ClassB = make_class()
    registry.register_singleton(ClassA(), ClassA)
    assert registry.find_factory(ClassB) is None
