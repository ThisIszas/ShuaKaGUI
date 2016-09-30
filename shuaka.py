#coding:utf-8
import urllib
import urllib2
import re
from lxml import etree
import cookielib
import time


def get_real(info):
    pattern = "[^\s]+"
    real = re.findall(pattern, info, re.S)
    return real[0]


def get_x_selectoro(url):
    request = urllib2.urlopen(url)
    text = request.read()
    x_selector = etree.HTML(text)
    return x_selector


def get_useful_time(info, count):
    for each in info:
        useful_time = get_real(each)
        if useful_time == u"有效 ":
            count += 1
    return count


def get_cookies():
    cj = cookielib.LWPCookieJar()
    cookie_support = urllib2.HTTPCookieProcessor(cj)
    opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
    urllib2.install_opener(opener)


def zaocao(zao_cao_url, count):
    zc_selector = get_x_selectoro(zao_cao_url)
    zc_info = zc_selector.xpath('//div[@class="divHeight"]/table[@cellpadding="0"]/tr/td[6]/text()')
    for each in zc_info:
        useful_time = get_real(each)
        if useful_time == u"有效":
            count += 1
    list2 = []
    list2.append(len(zc_info))
    list2.append(count)
    return list2


def shangke(club_sk_url, count):
    sk_selector = get_x_selectoro(club_sk_url)
    sk_info = sk_selector.xpath('//div[@class="divHeight"]/table[@cellpadding="0"]/tr/td[7]/text()')
    for each in sk_info:
        useful_time = get_real(each)
        if useful_time == u"有效 ":
            count += 1
    list2 = []
    list2.append(len(sk_info))
    list2.append(count)
    return list2


def pingshishuaka_1(stsuzhi_sk_url, count):
    sttz_selector = get_x_selectoro(stsuzhi_sk_url)
    sttz_info = sttz_selector.xpath('//div[@class="divHeight"]/table[@cellpadding="0"]/tr/td[7]/text()')
    count = get_useful_time(sttz_info, count)
    list2 = []
    list2.append(len(sttz_info))
    list2.append(count)
    return list2


def pingshishuaka_2(zizhuxuexi_sk_url, count):
    zzxx_selector = get_x_selectoro(zizhuxuexi_sk_url)
    zzxx_info = zzxx_selector.xpath('//div[@class="divHeight"]/table[@cellpadding="0"]/tr/td[7]/text()')
    count = get_useful_time(zzxx_info, count)
    # next_page_url = ..............
    # if next_page_url:
    #     pingshishuaka_2(next_page_url,count)
    list2 = []
    list2.append(len(zzxx_info))
    list2.append(count)
    return list2

def get_info(user_name, pw):
    get_cookies()
    login_ulr = "http://172.16.51.37/user_login.html"
    host_url = "http://172.16.51.37/"
    urllib2.urlopen(host_url)
    post_data = {
        "loginName": user_name,
        "password": pw
    }
    post_data = urllib.urlencode(post_data)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)\
     Chrome/52.0.2743.116 Safari/537.36',
               'Referer': 'http://172.16.51.37/'}
    request = urllib2.Request(login_ulr, post_data, headers)
    response = urllib2.urlopen(request)
    body = response.read()
    flag = re.findall(".用户名或密码不正确", body, re.S)
    if flag:
        return "error101"
    selector = etree.HTML(body)
    name = selector.xpath('//div[@id="accordion1"]/div[@style="display:none"]/table[@width="100%"]/tr/td\
    [@style="font-size:12px"]/text()')
    rname = name[3]
    pattern = "[^\s]+"
    rname = re.findall(pattern, rname, re.S)
    real_name = rname[0]
    return real_name

