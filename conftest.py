import pytest

def pytest_addoption(parser):
    parser.addoption("--name", action="store", default="default name")

@pytest.fixture(scope="session")
def name(request):
    return request.config.getoption("--name")
