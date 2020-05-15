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

# import orig library
from manuplate_ftp import ManuplateFTP
import ftpdelconfig

#
# logging setting.
#
import logging
import traceback
LOGGING_FILE = "ftplog.txt"
logging.basicConfig(filename=LOGGING_FILE, level=logging.DEBUG)

#console output message level is info.
#default(file) message level is debug.
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

#main module logger
logger_main = logging.getLogger(__name__)

#
# FTP Server Info (FTPS)
#
FTP_HOST     = 'localhost'
FTP_ACCOUNT  = 'anonymous'
FTP_PASSWORD = 'anonymous'
FTP_DIR      = '/'
FTP_DEL_LIST_FILE = 'DEFAULTFILE'

#
# FTP delete file start index
#
FTP_DEL_START_INDEX = 0


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

def get_ftp_delete_file_list(readfile):
    try:
        content_list = []
        for line in open(readfile,'r',encoding="utf-8_sig"):
            line = line.replace('\n','')
            line = line[:-3]
            content_list.append(line)

        #delete duplicate data.        
        content_list = sorted(set(content_list), key=content_list.index)

        return content_list
    except Exception as e:
        logger_main.error('%s %s %s', datetime.datetime.now(), sys._getframe().f_code.co_name, e)
        return None

def modify_delete_file_name(content_list):
    try:
        delete_file_name = []
        for fname in content_list:
            for i in range(1,43,1):
                delete_file_name.append(str(i) + '/' + fname)
            delete_file_name.append('C' + '/' + fname)
            delete_file_name.append('D' + '/' + fname)
            delete_file_name.append('L' + '/' + fname)
            delete_file_name.append('S' + '/' + fname)

        return delete_file_name
    except Exception as e:
        logger_main.error('%s %s %s', datetime.datetime.now(), sys._getframe().f_code.co_name, e)
        return None


if __name__ == '__main__':

    #logging
    logger_main.info('%s program start.', datetime.datetime.now())

    #get file candidate list
    delete_contents = get_ftp_delete_file_list(FTP_DEL_LIST_FILE)
    delete_contents = modify_delete_file_name(delete_contents)
    logger_main.info('%s program delete file list up finish.' % datetime.datetime.now())


    #make ftp class
    session = ManuplateFTP()
    #connect ftpserver
    if session.Create_SessionFTPS(FTP_HOST,FTP_ACCOUNT,FTP_PASSWORD) < 0 :
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
        retry_count = 3
        while retry_count > 0:
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
                retry_count = 0
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
                if retry_count < 0 : exit(1)   

    session.ftp_quit()
    logger_main.info('%s %s program end. ', datetime.datetime.now(), sys._getframe().f_code.co_name)
                
