from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def tests_path():
    return Path(__file__).parent
