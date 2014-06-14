# -*- coding: gbk -*-
import urllib2,urllib,cookielib,json

class kpSign(object):
    username = ''
    password = ''
    #登录显示页面
    indexurl = 'https://www.kuaipan.cn/account_login.htm'
    #登录的form表单url
    loginurl = 'https://www.kuaipan.cn/index.php?ac=account&op=login'
    #签到的真正url
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
            msg = "网络链接错误"
            return (False,msg)
        response = urllib2.urlopen(req)        
        # str to dict
        login= eval(response.read())
        if login['state'] == '0' :
            msg = "登录失败:%s" % (login["errcode"])
            return (False,msg)
        else:                
            msg = "登录成功,准备签到！"
            return (True,msg)

    def sign(self):
        response = urllib2.urlopen(self.signurl)
        sign = response.read()
        l = json.loads(sign)
        if (l and l['state'] == 1) or \
        (l and 0 == l['state'] and l['increase'] * 1 == 0 and l['monthtask'].M900 == 900):
            msg = "恭喜你签到成功！"
            k = l['increase']*1
            m = l['rewardsize'] * 1
            if (k == 0 and l['monthtask'].M900 == 900):
                msg = "本月签到积分已领取完成"
            else:
                msg = "签到奖励积分:%s" % (k)
            if m == 0:
                msg = "手气太不好了！奖励 0M 空间"
            else:
                msg = "签到奖励空间：%sM" % (m)
        else:
            if (l['state'] == -102):
                msg = "今天您已经签到过了"
            else:
                msg = "签到失败，遇到网络错误，请稍后再试！"
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

