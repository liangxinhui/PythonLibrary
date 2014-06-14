# -*- coding: cp936 -*-
import urllib2,urllib
import re

phoneNum = "14500000000"

#获取已用流量总量
def getUsedTraficTotal(phoneNum):
    userinfo_url = "http://3g10010.net/load_userinfo.php"
    post_data = {"user_name":phoneNum}
    req=urllib2.Request(userinfo_url,urllib.urlencode(post_data))
    response = urllib2.urlopen(req).read()
    #get trafic total
    traffic_total = "Unknow"
    match = re.search('"traffic_total">(.*?)<', response)
    if match:
            traffic_total = match.groups()[0]    
    return response,traffic_total

#获取流量详情
def getDetailTrafic():
    detail_url = "http://3g10010.net/account_info.php?userid="+ phoneNum + "&host=38118&quota=6"
    detail = urllib2.urlopen(detail_url).read()
    return detail
    



print getUsedTraficTotal(phoneNum)
print getDetailTrafic()
