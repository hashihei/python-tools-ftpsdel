#
#
# RefURL: https://docs.pytest.org/en/latest/example/parametrize.html
#
#

#
# import
#
import pytest

def pytest_addoption(parser):
    """Add pytest command options."""

    #RefURL: https://docs.python.org/3/library/argparse.html#the-add-argument-method
    parser.addoption(
        "--host",
        action="store",
        default="localhost",
        help="set ftps server ip address"
    )
    parser.addoption(
        "--account",
        action="store",
        default="anonymous",
        help="set ftps username"
    )
    parser.addoption(
        "--password",
        action="store",
        default="password",
        help="set ftps password"
    )

@pytest.fixture
def cli_host(request):
    print(request.config.getoption('--host'))
    return request.config.getoption('--host')

@pytest.fixture
def cli_account(request):
    print(request.config.getoption('--account'))
    return request.config.getoption('--account')

@pytest.fixture
def cli_password(request):
    print(request.config.getoption('--password'))
    return request.config.getoption('--password')
