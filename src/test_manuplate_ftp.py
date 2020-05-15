#
#import 
#
import pytest
import os
#orig class
import manuplate_ftp
import ftpdelconfig


def test_create_class():
    session = manuplate_ftp.ManuplateFTP()

    assert session is not None

def test_Output_Error():
    session = manuplate_ftp.ManuplateFTP()

    assert session.Output_Error('funcname',Exception()) == 0

def test_Output_Error_onlyMSG():
    session = manuplate_ftp.ManuplateFTP()

    assert session.Output_Error_onlyMSG('funcname','testmsg') == 0

def test_get_auth_info(cli_conf):
    
    assert ftpdelconfig.get_ftps_HOST(cli_conf) is not None
    assert ftpdelconfig.get_ftps_USER(cli_conf) is not None
    assert ftpdelconfig.get_ftps_PASS(cli_conf) is not None
    assert ftpdelconfig.get_ftps_FTP_LOGIN_DIR(cli_conf) is not None
    assert ftpdelconfig.get_ftps_FTP_DEL_LIST_DIR(cli_conf) is not None
    assert ftpdelconfig.get_ftps_FTP_DEL_LIST_FILE(cli_conf) is not None


def test_Create_SessionFTPS(cli_conf):
    session = manuplate_ftp.ManuplateFTP()

    #get authentication set value.
    HOST = ftpdelconfig.get_ftps_HOST(cli_conf)
    ACCOUNT = ftpdelconfig.get_ftps_USER(cli_conf)
    PASSWORD = ftpdelconfig.get_ftps_PASS(cli_conf)

    assert session.Create_SessionFTPS(HOST,ACCOUNT,PASSWORD) == 0
    assert session.ftp_quit() == 0

def test_ftp_cwd(cli_conf):
    session = manuplate_ftp.ManuplateFTP()

    #get authentication set value.
    HOST = ftpdelconfig.get_ftps_HOST(cli_conf)
    ACCOUNT = ftpdelconfig.get_ftps_USER(cli_conf)
    PASSWORD = ftpdelconfig.get_ftps_PASS(cli_conf)

    assert session.Create_SessionFTPS(HOST,ACCOUNT,PASSWORD) == 0
    assert session.ftp_cwd('/') == 0
    assert session.ftp_quit() == 0

def test_ftp_nlst(cli_conf):
    session = manuplate_ftp.ManuplateFTP()

    #get authentication set value.
    HOST = ftpdelconfig.get_ftps_HOST(cli_conf)
    ACCOUNT = ftpdelconfig.get_ftps_USER(cli_conf)
    PASSWORD = ftpdelconfig.get_ftps_PASS(cli_conf)

    assert session.Create_SessionFTPS(HOST,ACCOUNT,PASSWORD) == 0
    assert session.ftp_nlst() is not None
    assert session.ftp_quit() == 0

def test_ftp_delete(cli_conf):
    session = manuplate_ftp.ManuplateFTP()

    #get authentication set value.
    HOST = ftpdelconfig.get_ftps_HOST(cli_conf)
    ACCOUNT = ftpdelconfig.get_ftps_USER(cli_conf)
    PASSWORD = ftpdelconfig.get_ftps_PASS(cli_conf)

    FILE_NAME = 'TESTFILE1.txt'
    TEST_FILE_PATH = 'img/goods/'

    assert session.Create_SessionFTPS(HOST,ACCOUNT,PASSWORD) == 0
    assert session.ftp_cwd('/') == 0
    with open(FILE_NAME, 'rb') as f:
        session.ftp_session.storbinary('STOR /img/goods/TESTFILE1.txt', f)
    assert session.ftp_nlst(FILE_NAME) is not None
    assert session.ftp_delete(FILE_NAME) == 0
    assert session.ftp_quit() == 0


