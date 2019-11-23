import pytest

from wired import ServiceRegistry


@pytest.fixture
def settings():
    from tutorials.dcdi.decorators.models import Settings

    settings = Settings(punctuation='!!')
    return settings


@pytest.fixture
def registry(settings):
    from tutorials.dcdi.decorators import app_bootstrap

    r: ServiceRegistry = app_bootstrap(settings)
    return r


def test_sample_interactions(registry):
    from tutorials.dcdi.decorators import sample_interactions

    greetings = sample_interactions(registry)
    # Let's test that the request.url got injected correctly
    assert 'mary: Hello Mary !!' == greetings[0]
    assert 'henri and FrenchView: Bonjour Henri !!' == greetings[1]
