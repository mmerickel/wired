import os
import pytest
import sys


@pytest.fixture(scope="session", autouse=True)
def docs_path():
    tutorial_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '../../../docs')
    )
    sys.path.insert(0, tutorial_path)
