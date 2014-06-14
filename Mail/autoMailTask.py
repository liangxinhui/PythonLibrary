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
    # ����һ��pop3�������ʱ��ʵ�����Ѿ������Ϸ�������
    self.pp = poplib.POP3_SSL(server)
    # ������������û���
    print self.pp.user(username)
    # ���������������
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
          if not par.is_multipart(): # ����Ҫ�ж��Ƿ���multipart���ǵĻ�����������������õģ�����Ϊʲô�����˽�mime���֪ʶ��
              name = par.get_param("name") #����Ǹ���������ͻ�ȡ���������ļ���

              if name:
                  #�и���
                  #print '�и���'+fname
                  data = par.get_payload(decode=True) #��������������ݣ�Ȼ��洢���ļ���
                  atta[fname]=data
                  # ��������д���ֻ��Ϊ�˽�����=?gbk?Q?=CF=E0=C6=AC.rar?=�������ļ���
                  h = email.Header.Header(name)
                  dh = email.Header.decode_header(h)
                  fname = dh[0][0]

                  """
                  try:
                      f = open(fname, 'wb') #ע��һ��Ҫ��wb�����ļ�����Ϊ����һ�㶼�Ƕ������ļ�
                  except:
                      print '�������зǷ��ַ����Զ���һ��'
                      f = open('aaaa', 'wb')
                  f.write(data)
                  f.close()
                  """
              else:
                  #���Ǹ��������ı�����
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

