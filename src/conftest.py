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
        "--change-conf",
        action="store",
        default="ftpdel.conf",
        help="ftpdel setting file"
    )

@pytest.fixture
def cli_conf(request):
    return request.config.getoption('--change-conf')
