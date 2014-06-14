#-*- encoding: gb2312 -*-

import os, sys, string
import poplib
import email

class AutoMailTask():
  # init
  #def __init__(self):
  #  self.pp

  # logIn  
  def logIn(self,server, username, password):
    # 创建一个pop3对象，这个时候实际上已经连接上服务器了
    self.pp = poplib.POP3_SSL(server)
    # 向服务器发送用户名
    print self.pp.user(username)
    # 向服务器发送密码
    print self.pp.pass_(password)
    return
  
  # stat
  def stat(self):
    return self.pp.stat()

  # get Subject
  def getSubject(self,index):
    msg = self.pp.top(index,0)
    m = email.message_from_string(string.join(msg[1],'\n'))
    return email.Header.decode_header(m['subject'])[0][0]

  # get an email in type "email"
  def getMail(self, index):
    down = self.pp.retr(index)
    return email.message_from_string(string.join(down[1],'\n'))
  
  # quit
  def quit(self):
    return self.pp.quit()
  
  def parseMail(self,mail):
    textplain=''
    texthtml=''
    atta={}
    if mail.is_multipart():
        for par in mail.walk():
          if not par.is_multipart(): # 这里要判断是否是multipart，是的话，里面的数据是无用的，至于为什么可以了解mime相关知识。
              name = par.get_param("name") #如果是附件，这里就会取出附件的文件名

              if name:
                  #有附件
                  #print '有附件'+fname
                  data = par.get_payload(decode=True) #　解码出附件数据，然后存储到文件中
                  atta[fname]=data
                  # 下面的三行代码只是为了解码象=?gbk?Q?=CF=E0=C6=AC.rar?=这样的文件名
                  h = email.Header.Header(name)
                  dh = email.Header.decode_header(h)
                  fname = dh[0][0]

                  """
                  try:
                      f = open(fname, 'wb') #注意一定要用wb来打开文件，因为附件一般都是二进制文件
                  except:
                      print '附件名有非法字符，自动换一个'
                      f = open('aaaa', 'wb')
                  f.write(data)
                  f.close()
                  """
              else:
                  #不是附件，是文本内容
                  content_type= par.get_content_type()
                  charset = par.get_charset()
                  if content_type in ['text/plain']:
                      if charset==None:
                          textplain=par.get_payload(decode=True)
                      else:
                          textplain=par.get_payload(decode=True).decode(charset)
                  if content_type in ['text/html']:
                      if charset==None:
                          texthtml=par.get_payload(decode=True)
                      else:
                          texthtml=par.get_payload(decode=True).decode(charset)
    else:
      type=mail.get_content_charset()
      if type==None:
          textplain=mail.get_payload()
      else:
          try:
              textplain=unicode(mail.get_payload(),type)
          except UnicodeDecodeError:
              textplain='Error'

    return (textplain,texthtml,atta)


if __name__ == '__main__':
  import getpass
  server = raw_input("server:")
  username = raw_input("username:")
  passwd = getpass.getpass("password:")


  amt = AutoMailTask()
  # log In
  amt.logIn(server, username, passwd)

  # get Stat
  mailCount, mailSize = amt.stat()
 
  for i in range(mailCount):
    subject = amt.getSubject(i+1)
    if subject == "gmailTitle" :
      m = amt.getMail(i+1)
      mailContent = amt.parseMail(m)
      print mailContent[0]

  amt.quit()

