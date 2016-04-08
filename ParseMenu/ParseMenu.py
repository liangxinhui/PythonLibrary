# -*- coding: gbk -*-

############################################
#@brief   解析txt目录，转为FreePic2Pdf外挂格式
#@date    2016-04-08
#@author  liangxinhui@qq.com
############################################

import re

def ParseFile(filePath):
	fin = open(filePath, 'r')
	for line in fin:
		line = line.lstrip('\r\n ')
		line = line.rstrip('\r\n ')
		#match = re.search(r"^([\d. ]+)?(.*?)([\d]+)$", line, re.MULTILINE)
		match = re.search(r"^((?:[\d.]+)|(?:第\d+章)|(?:附录(?:[A-Z])?(?:[\d]+)?))? *(.*?)([\d]+) *$", line, re.MULTILINE)		
		if match:
			sectionNumStr = match.group(1) or ''
			titleStr = match.group(2)
			pageNum = match.group(3)
			tabCount = sectionNumStr.count('.')
			linePrefix = ''
			if tabCount > 0:
				linePrefix = '\t' * tabCount
			line = linePrefix + sectionNumStr + ' ' +  titleStr + '\t' + pageNum
		print line
	
	
import os
import sys
def ShowUsage():
	print """usage:\n  %s menu.txt""" %(os.path.basename(__file__))
	

if __name__ == '__main__':
	if len(sys.argv) < 2:
		ShowUsage()
		exit(0)
	filePath = sys.argv[1]
	if not os.path.exists(filePath):
		print 'FileNotExsit:', filePath
		exit(0)
	ParseFile(filePath)