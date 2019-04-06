import os
import sys

import pytest


@pytest.fixture(scope="session", autouse=True)
def docs_path():
    tutorial_path = os.path.relpath('../../docs/tutorial', __file__)
    sys.path.append(tutorial_path)
