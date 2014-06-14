# -*- coding: gbk -*-
import urllib2,urllib,cookielib,json

class kpTurnPlate(object):
    def __init__(self):
        self.headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Referer': 'http://huodong.kuaipan.cn/turnplate/',
        'Origin':'http://huodong.kuaipan.cn',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36'
        }

    def __freshLottey__(self):
        url = "http://huodong.kuaipan.cn/ajaxTurnplate/freshLottery/"
        urllib2.urlopen(url)

    def __lottery__(self):
        lotteryurl = "http://huodong.kuaipan.cn/ajaxTurnplate/lottery/"
        post_data = {}
        req=urllib2.Request(lotteryurl,urllib.urlencode(post_data),self.headers)
        lotteryResponse = urllib2.urlopen(req)
        #lotteryResponse = urllib2.urlopen(lotteryurl,{},headers)
        lotteryResponseJson = json.loads(lotteryResponse.read())
        print "lotteryResponseJson:",type(lotteryResponseJson),lotteryResponseJson
        if(lotteryResponseJson['status'] == 'ok'):
            print "awardType:",type(lotteryResponseJson['data']['awardType']),lotteryResponseJson['data']['awardType']
            msg =  "恭喜你，抽中了：%s"%(lotteryResponseJson['data']['awardType'])
            print "msg:",type(msg),msg
            return msg
        else:
            if(lotteryResponseJson['status'] == 'noChance'):
                msg = '今天已经抽过奖了，明天再来吧.'
                return msg
            else:
                msg = "Error, lotteryResponse:",lotteryResponseJson
                return msg
                
    def turnplate(self):
        self.__freshLottey__()
        return self.__lottery__()

    def login(self,username,password):
        url = "http://huodong.kuaipan.cn/turnplate/"
        loginurl = "http://huodong.kuaipan.cn/account/login/"
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        urllib2.install_opener(opener)
        try:
            urllib2.urlopen(url)
            post_data = {'loginId':username,'password':password}
            req=urllib2.Request(loginurl,urllib.urlencode(post_data),self.headers)
        except Exception, e:
            msg = "网络链接错误"+e.message
            return (False,msg)
        loginResponse = urllib2.urlopen(req)
        loginResponseJson = json.loads(loginResponse.read())
        if(loginResponseJson and loginResponseJson['status'] == 'ok'):
            msg = "Login Success"
            return (True,msg)
        else:
            msg = "LoginFailed:",loginResponseJson['status'],loginResponseJson['data']
            return (False,msg)


if __name__ == "__main__":
    username = raw_input("username:")
    password = raw_input("password:")
    myTurn = kpTurnPlate()
    bLogin,msg = myTurn.login(username,password)
    print msg
    if(bLogin):
        msg = myTurn.turnplate()
        print msg
            
            
        






