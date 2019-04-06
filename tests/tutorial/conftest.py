import os
import sys

import pytest

pytestmark = pytest.mark.skipif(sys.version_info < (3, 7),
                                reason="requires python3.7")


@pytest.fixture(scope="session", autouse=True)
def docs_path():
    tutorial_path = os.path.abspath(os.path.join(
        os.path.dirname(__file__),
        '../../docs/tutorial',
    ))
    sys.path.insert(0, tutorial_path)
