# -*- coding: utf-8 -*-
import win32api,win32con

#将Python脚本高亮显示，并传至Evernote


import sys
if len(sys.argv) > 1:
    print sys.argv[1]
    fileName = sys.argv[1]
else :
    win32api.MessageBox(0, u"输入参数有误", u"",win32con.MB_ICONERROR)
    exit(1)
    
    
auth_token = "your_evernote_auth_key"


def highLightPython(code):
    from pygments import highlight
    from pygments.lexers import PythonLexer
    from pygments.formatters import HtmlFormatter
    # Note: noclasses(without css)
    formatedCode = highlight(code, PythonLexer(), HtmlFormatter(noclasses=True))
    return formatedCode.replace('class="highlight" ','')


def makeEMXL(text):
    content = '<?xml version="1.0" encoding="UTF-8"?>'
    content += '<!DOCTYPE en-note SYSTEM ' \
        '"http://xml.evernote.com/pub/enml2.dtd">'
    content += '<en-note>'  + text.encode('utf-8')
    content += '</en-note>'
    return content


import hashlib
import binascii
#import evernote.edam.userstore.constants as UserStoreConstants
#import evernote.edam.type.ttypes as Types
#from evernote.api.client import EvernoteClient
try:
    # Note: sandbox=False, the DefaultValue is True
    # client = EvernoteClient(token=auth_token, sandbox=False)
    # get the note_store
    # note_store = client.get_note_store()
    # create Note
    # note = Types.Note()
    # set title
    #note.title = fileName
    # set content
    code = open(fileName,'r').read().decode('utf-8')
    print code
    highLightedCode = highLightPython(code)
    print highLightedCode
    print fileName
    open(fileName+".html","w").write(highLightedCode)
    #note.content = makeEMXL(highLightedCode)
    # Upload Note
    #created_note = note_store.createNote(note)
    #print "Successfully created a new note with GUID: ", created_note.guid
    #win32api.MessageBox(0, u"添加成功", u"",win32con.MB_ICONASTERISK)
   
except Exception,e:   
    #msg = "%s: %s" %(Exception, e)
    #win32api.MessageBox(0, msg, u"Error",win32con.MB_OK)
    pass
