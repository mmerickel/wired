import pytest

from wired import ServiceRegistry


@pytest.fixture
def settings():
    from wired.samples.datastore import Settings
    settings = Settings(punctuation='!!')
    return settings


@pytest.fixture
def registry(settings):
    from wired.samples.datastore import app_bootstrap
    r: ServiceRegistry = app_bootstrap(settings)
    return r


def test_sample_interactions(registry):
    # Integration-style test

    from wired.samples.datastore import sample_interactions
    greetings = sample_interactions(registry)
    assert 'Hello Mary !!' == greetings[0]
    assert 'Bonjour Henri !!' == greetings[1]
