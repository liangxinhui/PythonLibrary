# -*- coding: cp936 -*-
import win32api,win32con
#win32api.MessageBox(0, msg, u"Error",win32con.MB_OK)
import urllib2
from bs4 import BeautifulSoup
from sendmail import send_mail


def getBookStatus(url):
    res = urllib2.urlopen(url).read()
    soup = BeautifulSoup(res,from_encoding="gb18030")
    return soup.findAll('table')[7].findAll('tr')[2].findAll('td')[5].text




if __name__ == '__main__':
    bookList = [{
                'url':'http://219.216.128.15:8080/book/detailBook.jsp?rec_ctrl_id=01h0124359',
                'name': u'python 科学计算'
            },
            {
                'url':'http://219.216.128.15:8080/book/detailBook.jsp?rec_ctrl_id=01h0124362',
                'name': u'Python Web开发学习实录'
            }]


    bIsAvailable = False
    result = ''
    for book in bookList:
        #print 'check...'
        status = getBookStatus(book['url'])
        #print status
        result += "%s:%s\n" % (book['name'],status)
        if status != u'编目中':
            bIsAvailable = True
            
    if bIsAvailable:
        server = {
                'name':'smtp.qq.com',
                'user':'361656549',
                'passwd':'xxx'
                }
        send_mail(server, '361656549@qq.com', ['liangxinhui@qq.com',],u'图书流通状态' , result, [])
        #print "mail sent"
    #else:
        #print result

win32api.MessageBox(0, result, u"",win32con.MB_OK)

