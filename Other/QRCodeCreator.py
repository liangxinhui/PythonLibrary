# -*- coding: utf-8 -*-
import win32api,win32con
import sys
if len(sys.argv) > 1:
    print sys.argv[1]
    fileName = sys.argv[1]
else :
    win32api.MessageBox(0, u"输入参数有误", u"",win32con.MB_ICONERROR)
    exit(1)
    

import webbrowser
import urllib2
text = open(fileName).read().decode('utf-8')
url = 'https://chart.googleapis.com/chart?cht=qr&chs=350x350&choe=UTF-8&chld=L|4&chl=%s' + urllib2.quote(text.encode('utf-8'))
# 用系统默认浏览器打开网页
webbrowser.open_new_tab(url)
