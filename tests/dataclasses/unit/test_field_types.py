import pytest

from wired.dataclasses import injected, InjectedArgumentException


class BogusResource:
    pass


def test_invalid_both_attr_and_key():
    with pytest.raises(InjectedArgumentException) as exc:
        injected(BogusResource, attr='title', key='name')
    msg = 'Cannot supply both attr and key arguments to inject'
    assert msg == str(exc.value)


def test_attr():
    i = injected(BogusResource, attr='title')
    assert BogusResource == i.metadata['injected']['type_']
    assert 'title' == i.metadata['injected']['attr']


def test_key():
    i = injected(BogusResource, key='title')
    assert BogusResource == i.metadata['injected']['type_']
    assert 'title' == i.metadata['injected']['key']


def test_call():
    i = injected(BogusResource, call=False)
    assert BogusResource == i.metadata['injected']['type_']
    assert False is i.metadata['injected']['call']


def test_default():
    i = injected(BogusResource)
    assert BogusResource == i.metadata['injected']['type_']
    assert True is i.metadata['injected']['call']


def test_other_data():
    # Ensure the field can have other stuff in it
    i = injected(BogusResource, attr='title', metadata=dict(a=1), init=False)
    assert BogusResource == i.metadata['injected']['type_']
    assert 'title' == i.metadata['injected']['attr']
    assert 1 == i.metadata['a']
    assert False is i.init
