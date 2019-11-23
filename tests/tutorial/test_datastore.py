import pytest

from wired import ServiceRegistry


@pytest.fixture
def settings():
    from tutorial.datastore import Settings

    settings = Settings(punctuation='!!')
    return settings


@pytest.fixture
def registry(settings):
    from tutorial.datastore import app_bootstrap

    r: ServiceRegistry = app_bootstrap(settings)
    return r


def test_sample_interactions(registry):
    from tutorial.datastore import sample_interactions

    greetings = sample_interactions(registry)
    assert 'Hello Mary !!' == greetings[0]
    assert 'Bonjour Henri !!' == greetings[1]
