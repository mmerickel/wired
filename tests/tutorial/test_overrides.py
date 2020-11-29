import pytest

from wired import ServiceRegistry


@pytest.fixture
def settings():
    from tutorial.overrides.models import Settings

    settings = Settings(punctuation='!!')
    return settings


@pytest.fixture
def registry(settings):
    from tutorial.overrides import app_bootstrap

    r: ServiceRegistry = app_bootstrap(settings)
    return r


def test_sample_interactions(registry):
    from tutorial.overrides import sample_interactions

    greetings = sample_interactions(registry)
    assert 'Override Mary !!' == greetings[0]
    assert 'Bonjour Henri !!' == greetings[1]


def test_main():
    from tutorial.overrides import main

    assert None is main()
