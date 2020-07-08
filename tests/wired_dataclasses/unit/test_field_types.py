from wired.dataclasses import injected


class BogusResource:
    pass


def test_attr():
    i = injected(BogusResource, attr='title')
    assert BogusResource == i.metadata['injected']['type_']
    assert 'title' == i.metadata['injected']['attr']


def test_name():
    i = injected(BogusResource, name='db')
    assert BogusResource == i.metadata['injected']['type_']
    assert 'db' == i.metadata['injected']['name']


def test_other_data():
    # Ensure the field can have other stuff in it
    i = injected(BogusResource, attr='title', metadata=dict(a=1), init=False)
    assert BogusResource == i.metadata['injected']['type_']
    assert '' == i.metadata['injected']['name']
    assert 'title' == i.metadata['injected']['attr']
    assert 1 == i.metadata['a']
    assert False is i.init
