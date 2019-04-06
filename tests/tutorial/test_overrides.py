import sys

import pytest

from wired import ServiceRegistry


@pytest.fixture
def settings():
    from overrides import Settings
    settings = Settings(punctuation='!!')
    return settings


@pytest.fixture
def registry(settings):
    from overrides import app_bootstrap
    r: ServiceRegistry = app_bootstrap(settings)
    return r


@pytest.mark.skipif(sys.version_info < (3, 7),
                    reason="requires python3.3")
def test_sample_interactions(registry):
    # Integration-style test

    from overrides import sample_interactions
    greetings = sample_interactions(registry)
    assert 'Override Mary !!' == greetings[0]
    assert 'Bonjour Henri !!' == greetings[1]
