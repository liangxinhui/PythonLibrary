# -*- coding: gbk -*-
import urllib2,urllib,cookielib,json

class kpSign(object):
    username = ''
    password = ''
    #��¼��ʾҳ��
    indexurl = 'https://www.kuaipan.cn/account_login.htm'
    #��¼��form��url
    loginurl = 'https://www.kuaipan.cn/index.php?ac=account&op=login'
    #ǩ��������url
    signurl = 'http://www.kuaipan.cn/index.php?ac=common&op=usersign'
    #http://www.pm2d5.com/chajian/41_pic.html

    def __init__(self,username,password):
        self.username = username
        self.password = password

    def login(self):
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        urllib2.install_opener(opener)
        try:
            urllib2.urlopen(self.indexurl)
            post_data = {'username':self.username,'userpwd':self.password,'isajax':'yes'}
            req=urllib2.Request(self.loginurl,urllib.urlencode(post_data))
        except Exception, e:
            msg = "�������Ӵ���"
            return (False,msg)
        response = urllib2.urlopen(req)        
        # str to dict
        login= eval(response.read())
        if login['state'] == '0' :
            msg = "��¼ʧ��:%s" % (login["errcode"])
            return (False,msg)
        else:                
            msg = "��¼�ɹ�,׼��ǩ����"
            return (True,msg)

    def sign(self):
        response = urllib2.urlopen(self.signurl)
        sign = response.read()
        l = json.loads(sign)
        if (l and l['state'] == 1) or \
        (l and 0 == l['state'] and l['increase'] * 1 == 0 and l['monthtask'].M900 == 900):
            msg = "��ϲ��ǩ���ɹ���"
            k = l['increase']*1
            m = l['rewardsize'] * 1
            if (k == 0 and l['monthtask'].M900 == 900):
                msg = "����ǩ����������ȡ���"
            else:
                msg = "ǩ����������:%s" % (k)
            if m == 0:
                msg = "����̫�����ˣ����� 0M �ռ�"
            else:
                msg = "ǩ�������ռ䣺%sM" % (m)
        else:
            if (l['state'] == -102):
                msg = "�������Ѿ�ǩ������"
            else:
                msg = "ǩ��ʧ�ܣ���������������Ժ����ԣ�"
        return msg


if __name__ == "__main__":
    username = raw_input("username:")
    password = raw_input("password:")    
    sign = kpSign(username,password)
    bLogin,msg = sign.login()
    print msg
    if bLogin:
        msg = sign.sign()
        print msg

