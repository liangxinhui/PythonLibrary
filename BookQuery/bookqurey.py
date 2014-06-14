# encoding=utf8

#以大连图书馆为例

import urllib2,urllib
import re

import sys
sysEncodeing = 'gbk'

while True :
   keyWords = raw_input("\nKeywords:").decode(sysEncodeing).encode('utf-8')
   if keyWords :
      mainPageURL = 'http://124.93.240.186/uhtbin/webcat/Unicode/0/49'
      mainPageContent = urllib2.urlopen(mainPageURL)                  
      match = re.search('<form name="searchform" method="post" action="(?P<action>.*?)">', mainPageContent.read())
      if match:
         qureyURL = 'http://124.93.240.186' + match.group('action')
         post_data = 'searchdata1=%s&srchfield1=TI^TITLE^SERIES^Title Processing^题名&library=ALL&sort_by=ANY' % keyWords
         req = urllib2.Request(qureyURL, post_data)
         qureyResult = urllib2.urlopen(req)
         for match in re.finditer(r'<li><h4 title="Search Result #[\d]+">Search Result #(?P<book_id>[\d]+)\. (?P<book_detail>.*?)</h4></li>', qureyResult.read()):
             print "%s:%s" %(match.group('book_id'),match.group('book_detail').decode('utf-8').encode(sysEncodeing))
   else :
      break
    
