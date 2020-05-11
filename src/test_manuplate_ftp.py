import manuplate_ftp
import pytest
import os

def test_create_class():
    session = manuplate_ftp.ManuplateFTP()

    assert session is not None

def test_Output_Error():
    session = manuplate_ftp.ManuplateFTP()

    assert session.Output_Error('funcname',Exception()) == 0

def test_Output_Error_onlyMSG():
    session = manuplate_ftp.ManuplateFTP()

    assert session.Output_Error_onlyMSG('funcname','testmsg') == 0

def test_Create_SessionFTPS(cli_host, cli_account, cli_password):
    session = manuplate_ftp.ManuplateFTP()

    HOST = cli_host
    ACCOUNT = cli_account
    PASSWORD = cli_password

    assert session.Create_SessionFTPS(HOST,ACCOUNT,PASSWORD) == 0
    assert session.ftp_quit() == 0

def test_ftp_cwd(cli_host, cli_account, cli_password):
    session = manuplate_ftp.ManuplateFTP()

    HOST = cli_host
    ACCOUNT = cli_account
    PASSWORD = cli_password

    assert session.Create_SessionFTPS(HOST,ACCOUNT,PASSWORD) == 0
    assert session.ftp_cwd('/') == 0
    assert session.ftp_quit() == 0

def test_ftp_nlst(cli_host, cli_account, cli_password):
    session = manuplate_ftp.ManuplateFTP()

    HOST = cli_host
    ACCOUNT = cli_account
    PASSWORD = cli_password

    assert session.Create_SessionFTPS(HOST,ACCOUNT,PASSWORD) == 0
    assert session.ftp_nlst() is not None
    assert session.ftp_quit() == 0

def test_ftp_delete(cli_host, cli_account, cli_password):
    session = manuplate_ftp.ManuplateFTP()

    HOST = cli_host
    ACCOUNT = cli_account
    PASSWORD = cli_password

    FILE_NAME = 'TESTFILE'
    assert session.Create_SessionFTPS(HOST,ACCOUNT,PASSWORD) == 0
    with open(FILE_NAME, 'rb') as f:
        session.ftp_session.storbinary('STOR ' + FILE_NAME, f)
    assert session.ftp_nlst(FILE_NAME) is not None
    assert session.ftp_delete(FILE_NAME) == 0
    assert session.ftp_quit() == 0


