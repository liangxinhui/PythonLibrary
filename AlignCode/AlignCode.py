# -*- coding: cp936 -*-

#######################################################################
#
#                 对齐代码（主要用于errorcode文件的对齐）
#
#######################################################################


def ShowUsage():
	print 'Usage:'
	print '       AlignCode RawFile [AlignedFile]'
	print '       the default AlignedFile is Aligned_RawFile'
	return

#######################################################################

import re
import sys

KEY_WORD_LIST = ';=,'


class LineInfo:
	def __init__(self, lineNo, rawText):
		self.LineNo  = lineNo
		self.RawText     = rawText
		# valid code = not comment && not empty line
		self.IsValidCode = False 
		self.ItemList	 = []
		self._Parse()
		return
	def _Parse(self):
		self.IsValidCode = self._IsValidCode()
		if self.IsValidCode:
			self.ItemList = self._GetItemListFromLine(self.RawText)
		return
	def _IsValidCode(self):
		cleanText = self.RawText.strip()
		if len(cleanText) == 0:
			return False
		# comment is not valid. (not exact, but enough)
		if cleanText.startswith('/') or cleanText.startswith('*') or cleanText.startswith('#'):
			return False
		return True
	def _GetItemListFromLine(self,lineRawText = ''):
		# fix rawText, add ' ' before and after [=;,]
		fixedText = re.sub("([%s])"%(KEY_WORD_LIST), r" \1 ", lineRawText)
		itemList = re.split("[\t ]", fixedText)
		itemList = [v for v in itemList if v!='']
		return itemList

def ParseLines(textLines = ['',]):
	retLineInfoList = []
	iLineNo = 0
	for line in textLines:
		curLineInfo = LineInfo(iLineNo,line)
		iLineNo += 1
		retLineInfoList.append(curLineInfo)
	return retLineInfoList

def GetMaxLengthList(lineInfoList = []):
	# 100 items in a row is enough
	retMaxLengthList = [0  for i in range(100)]
	for l in lineInfoList:
			iCurItem = 0                        
			for item in l.ItemList:
				if item not in KEY_WORD_LIST:
					curLen = len(item)
					if retMaxLengthList[iCurItem] < curLen:
						retMaxLengthList[iCurItem] = curLen
					iCurItem += 1
	#
	retMaxLengthList = [v for v in retMaxLengthList if v > 0]
	return retMaxLengthList


def CreateAlignLine(itemList, MaxLengthList):
	retLineText = ''
	iCurItem = 0
	for item in itemList:
		if item == '=':
			retLineText += ' = ' # before and after
		elif item == ',':
			retLineText += ', '	 # after
		elif item == ';':
			retLineText += ';'   # none
			retLineText = re.sub("[ ]*;", ";", retLineText)
		else:		
			curItemLength = MaxLengthList[iCurItem]+1
			if curItemLength > 20:
				curItemLength += 5
			formatText = '%%-%ds'%(curItemLength)
			retLineText += formatText%(item)
			iCurItem += 1 # not count [=,;]
	retLineText = retLineText.strip(' ')
	return retLineText


def AlignLineInfoList(lineInfoList = [], MaxLengthList=[]):
	retText = ""
	for line in lineInfoList:
		if line.IsValidCode:
			AlignedCode = CreateAlignLine(line.ItemList, MaxLengthList)
		else:
			AlignedCode = line.RawText
		retText += AlignedCode
	return retText



if __name__ == '__main__':	
	# Check Args
	if len(sys.argv) < 2:
		ShowUsage()
		exit(-1)		
	inputFile = sys.argv[1] 
	if len(sys.argv) > 2:
		outputFile = sys.argv[2]
	else:
		outputFile = 'Aligned_'+inputFile
	# Deal Align
	textLines = open(inputFile,'r').readlines()
	lineInfoList = ParseLines(textLines)
	lengthList = GetMaxLengthList(lineInfoList)
	retText = AlignLineInfoList(lineInfoList, lengthList)
	open(outputFile,'w').write(retText)
	print 'Done.\nOutputFile:',outputFile
