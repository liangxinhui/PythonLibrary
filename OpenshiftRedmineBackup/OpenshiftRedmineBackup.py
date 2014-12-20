###############################
#   liangxinhui@qq.com
###############################
import os
import time

###############################
#         Config
###############################

DROPBOX_UPLOADER_PATH = './dropbox_uploader.sh'
TMP_DIR = 'tmp/'
APP_NAME = os.environ.get('OPENSHIFT_APP_NAME')
CUR_TIME = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))

MAIN_ZIP_FILE_NAME = '%s_backup_%s.zip'%(APP_NAME,CUR_TIME)
REPO_FILE_NAME = 'RepoFiles.zip'
DATABASE_FILE_NAME = APP_NAME + '.sql'

###############################
#         Helper
###############################
def zipFileList(fileList, outputFile):
	strCmd = 'zip -r9 %s %s'%(outputFile, ' '.join(fileList))
	os.system(strCmd)
	return

def BackupDatabase(backupFile):
	host = os.environ.get('OPENSHIFT_MYSQL_DB_HOST')
	port = os.environ.get('OPENSHIFT_MYSQL_DB_PORT')
	username = os.environ.get('OPENSHIFT_MYSQL_DB_USERNAME')
	password = os.environ.get('OPENSHIFT_MYSQL_DB_PASSWORD')
	dbname = os.environ.get('OPENSHIFT_APP_NAME')
	strCmd = 'mysqldump -h%s -P%s -u%s -p%s %s > %s'%(host,port,username,password,dbname,backupFile)
	os.system(strCmd)
	return

def SendToDropbox(fileFullPath, uploadFileName):
	strCmd = '%s upload %s %s'%(DROPBOX_UPLOADER_PATH,fileFullPath,uploadFileName)
	os.system(strCmd)
	return
	
def ClearTmp():	
	strCmd = 'rm -rf %s*'%(TMP_DIR)
	os.system(strCmd)	
	return
	
###############################
#         Main
###############################
if __name__ == '__main__':
	# clear tmp folder
	ClearTmp()
	# make paths
	OPENSHIFT_REPO_DIR = os.environ.get('OPENSHIFT_REPO_DIR')
	REDMINE_FILES_LIST = [
		OPENSHIFT_REPO_DIR + 'files',
		OPENSHIFT_REPO_DIR + 'plugins',
		OPENSHIFT_REPO_DIR + 'public/themes'
	] 
	SQL_FILE_FULL_PATH = TMP_DIR + DATABASE_FILE_NAME
	ZIP_REPO_FILE_FULL_PATH = TMP_DIR + REPO_FILE_NAME
	ZIP_MAIN_FILE_FULL_PATH = TMP_DIR + MAIN_ZIP_FILE_NAME
	# backup step 1 -- database 
	BackupDatabase(SQL_FILE_FULL_PATH)
	# backup step 2 -- repofiles 
	zipFileList(REDMINE_FILES_LIST, ZIP_REPO_FILE_FULL_PATH)	
	# backup step 3 -- pack all in one file 
	Main_List = [ZIP_REPO_FILE_FULL_PATH, SQL_FILE_FULL_PATH]
	zipFileList(Main_List, ZIP_MAIN_FILE_FULL_PATH)
	# backup step 4 -- upload 
	SendToDropbox(ZIP_MAIN_FILE_FULL_PATH, MAIN_ZIP_FILE_NAME)	
	# clear tmp folder
	ClearTmp()

