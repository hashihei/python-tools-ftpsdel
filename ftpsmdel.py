#
# Copyright <2020> <hashihei>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

#
# Import library
#
import datetime
import sys
import os
from pathlib import Path
import logging
import traceback
import argparse

# import orig Class and Functions
from src.manuplate_ftp import ManuplateFTP
from src import ftpdelconfig

#
# logging setting.
#
LOGGING_FILE = ""


#WorkDir
WORKDIR = str(Path.cwd())
FOLDER_SIG = os.path.sep

#
# Add command arg.
#
parser = argparse.ArgumentParser()
parser.add_argument("--start_index", type=int, help="(int) file delete restart index. (optional)")
parser.add_argument("--config_file", type=str, help="(str) config file fully path. (optional)")
args = parser.parse_args()

#
# FTP delete file start index
#
if args.start_index is None:
    FTP_DEL_START_INDEX = 0
else:
    FTP_DEL_START_INDEX = int(args.start_index)

#
# FTPS Conf file
#
if args.config_file is None:
    CONFIG_FILE = WORKDIR + FOLDER_SIG + 'etc' + FOLDER_SIG + 'ftpdel.conf'
else:
    CONFIG_FILE = str(args.config_file)

#
# define for this program function. 
#
def get_auth_info(conf_path):

    if conf_path is None:
        HOST = ftpdelconfig.get_ftps_HOST()
        ACCOUNT = ftpdelconfig.get_ftps_USER()
        PASSWORD = ftpdelconfig.get_ftps_PASS()
    else:
        HOST = ftpdelconfig.get_ftps_HOST(conf_path)
        ACCOUNT = ftpdelconfig.get_ftps_USER(conf_path)
        PASSWORD = ftpdelconfig.get_ftps_PASS(conf_path)

    return HOST, ACCOUNT, PASSWORD

def get_ftp_delete_list(conf_path):
    if conf_path is None:
        DEL_LIST_DIR = ftpdelconfig.get_ftps_FTP_DEL_LIST_DIR()
        DEL_LIST_FILE = ftpdelconfig.get_ftps_FTP_DEL_LIST_FILE()
    else:
        DEL_LIST_DIR = ftpdelconfig.get_ftps_FTP_DEL_LIST_DIR(conf_path)
        DEL_LIST_FILE = ftpdelconfig.get_ftps_FTP_DEL_LIST_FILE(conf_path)

    return DEL_LIST_DIR, DEL_LIST_FILE

def get_ftp_delete_file_list(FTP_DEL_LIST_DIRS,FTP_DEL_LIST_FILES):
    try:
        content_list = []

        for line_dir in open(FTP_DEL_LIST_DIRS,'r',encoding='utf-8_sig'):
            if line_dir == '':
                pass
            elif line_dir[-1:] != '/':
                line_dir = line_dir + '/'
            for line_files in open(FTP_DEL_LIST_FILES,'r',encoding="utf-8_sig"):
                line_dir = line_dir.replace('\n','')
                line_files = line_files.replace('\n','')

                content_list.append(line_dir + line_files)

        return content_list
    except Exception as e:
        logger_main.error('%s %s %s', datetime.datetime.now(), sys._getframe().f_code.co_name, e)
        return None


if __name__ == '__main__':

    #
    #logging
    #
    LOGGING_FILE = ftpdelconfig.get_LOG_FILE(CONFIG_FILE)
    LOGGING_LEVEL = ftpdelconfig.get_LOG_LEVEL(CONFIG_FILE)

    logging.basicConfig(filename=LOGGING_FILE, level=logging.DEBUG)
    #console output message level is info.
    #default(file) message level is debug.
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(name)-20s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

    #main module logger
    logger_main = logging.getLogger(__name__)


    logger_main.info('%s program start.', datetime.datetime.now())

    #load setting
    FTP_HOST,FTP_ACCOUNT,FTP_PASSWORD = get_auth_info(CONFIG_FILE)
    FTP_DIR = ftpdelconfig.get_ftps_FTP_LOGIN_DIR(CONFIG_FILE)

    #get file candidate list
    FTP_DEL_LIST_DIR, FTP_DEL_LIST_FILE = get_ftp_delete_list(CONFIG_FILE)
    FTP_DEL_LIST_DIR = WORKDIR + FOLDER_SIG + FTP_DEL_LIST_DIR
    FTP_DEL_LIST_FILE = WORKDIR + FOLDER_SIG + FTP_DEL_LIST_FILE


    delete_contents = get_ftp_delete_file_list(FTP_DEL_LIST_DIR,FTP_DEL_LIST_FILE)

    logger_main.info('%s program delete file list up finish.' % datetime.datetime.now())

    #make ftp class
    session = ManuplateFTP()

    #connect ftpserver
    if session.Create_SessionFTPS(FTP_HOST,FTP_ACCOUNT,FTP_PASSWORD,True) < 0 :
        logger_main.error('%s FTP Connection error.', datetime.datetime.now())
        sys.exit(1)

    #set img root dir.
    if session.ftp_cwd(FTP_DIR) < 0 :
        logger_main.error('%s can not change directory to %s, exit program', datetime.datetime.now(),FTP_DIR)
        sys.exit(1)        

    #file delete.
    count = len(delete_contents)
    files = []

    for i, paths in enumerate(delete_contents):
        if i < FTP_DEL_START_INDEX:
            #ftps delete skip.
            continue
        #IF FTPS fail then retry 3 times.
        retry_count = 3
        while retry_count >= 0:
            if (i % 100 == 0):
                logger_main.info('%s %s file delete progress %s percent. (%d / %d)', datetime.datetime.now(), sys._getframe().f_code.co_name, str(round((i/count)*100,2)),i,count)

            #search file
            files = session.ftp_nlst(paths + '*')

            if files is not None:
                if len(files) > 0:
                    for f in files:
                        res = session.ftp_delete(f)
                    if res < 0 :
                        logger_main.error('%s %s %s delete failed.', datetime.datetime.now(), sys._getframe().f_code.co_name, f)
                    else:
                        logger_main.info('%s %s %s deleted.', datetime.datetime.now(), sys._getframe().f_code.co_name, f)
                #no retry. next list.
                retry_count = -1
            else:
                logger_main.info('%s %s %s delete failed. (file not found or aborted.)', datetime.datetime.now(), sys._getframe().f_code.co_name, paths)
                session.ftp_quit()
                #reconnect ftpserver
                logger_main.info('%s %s %s FTP login retry.', datetime.datetime.now(), sys._getframe().f_code.co_name, paths)
                if session.Create_SessionFTPS(FTP_HOST,FTP_ACCOUNT,FTP_PASSWORD) < 0 :
                    logger_main.error('%s FTP Connection error.', datetime.datetime.now())
                #set img root dir.
                if session.ftp_cwd(FTP_DIR) < 0 :
                    logger_main.error('%s can not change directory to %s, exit program', datetime.datetime.now(),FTP_DIR)
                retry_count = retry_count - 1                
                if retry_count < 0 :
                    exit(1)   

    session.ftp_quit()
    logger_main.info('%s %s program end. ', datetime.datetime.now(), sys._getframe().f_code.co_name)
                
