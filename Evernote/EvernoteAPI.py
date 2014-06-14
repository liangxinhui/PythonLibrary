# -*- coding: utf-8 -*-
import os

dirEvernote = "G:\\Program Files\\Evernote\\Evernote"
ENScript = "ENScript.exe"


def creatNote(title, text):
    import os
    command = r"%s\%s /i %s \r\n %s" %(dirEvernote, ENScript, title, text)
    print command
    print os.dpopen(command).read()
    



if __name__ == "__main__":
    from pygments import highlight
    from pygments.lexers import PythonLexer
    from pygments.formatters import HtmlFormatter
    code = open(u"F:\\金山快盘\\Python_Scripts\\EvernoteAPI.py",'r').read()
    formatedCode = highlight(code, PythonLexer(), HtmlFormatter(full=True))    
    creatNote("PythonCode",formatedCode.encode('utf-8'))
    
