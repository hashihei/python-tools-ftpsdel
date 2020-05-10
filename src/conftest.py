#
#
# RefURL: https://docs.pytest.org/en/latest/example/parametrize.html
#
#

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
        "--pass",
        action="store",
        default="",
        help="set ftps password"
    )

def pytest_generate_tests(metafunc):
    if "HOST" in metafunc.fixturenames:
        metafunc.parametrize("HOST",metafunc.config.getoption("--host"))

    if "ACCOUNT" in metafunc.fixturenames:
        metafunc.parametrize("ACCOUNT",metafunc.config.getoption("--account"))

    if "PASSWORD" in metafunc.fixturenames:
        metafunc.parametrize("PASSWORD",metafunc.config.getoption("--pass"))
