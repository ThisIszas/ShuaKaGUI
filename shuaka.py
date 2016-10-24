# coding:utf-8
import urllib
import urllib2
import re
from lxml import etree
import cookielib


def get_real(info):
    pattern = "[^\s]+"
    real = re.findall(pattern, info, re.S)
    if len(real) > 0:
        return real[0]


def get_x_selectoro(url, pn):
    post_data = {
        "pageNum": pn,
    }
    post_data = urllib.urlencode(post_data)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)\
     Chrome/52.0.2743.116 Safari/537.36',
               'Referer': 'http://172.16.51.37/'}
    request = urllib2.Request(url, post_data, headers)
    response = urllib2.urlopen(request)
    body = response.read()
    x_selector = etree.HTML(body)
    return x_selector


def get_useful_time(info, count):
    for each in info:
        useful_time = get_real(each)
        if useful_time == u"有效 " or useful_time == u"有效":
            count += 1
    return count


def get_cookies():
    cj = cookielib.LWPCookieJar()
    cookie_support = urllib2.HTTPCookieProcessor(cj)
    opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
    urllib2.install_opener(opener)


def next_page_flag(urls):
    response = urllib2.urlopen(urls)
    body = response.read()
    flag = re.findall('<option value=\"2\">', body, re.S)
    if len(flag) > 0:
        return 1
    else:
        return 0


def zaocao(zao_cao_url, count, pn=1, length=0):
    zc_selector = get_x_selectoro(zao_cao_url, pn)
    zc_info = zc_selector.xpath('//div[@class="divHeight"]/table[@cellpadding="0"]/tr/td[6]/text()')
    count = get_useful_time(zc_info, count)
    flag = next_page_flag(zao_cao_url)
    length += len(zc_info)
    list2 = [length, count]
    if flag and pn != 2:
        return zaocao(zao_cao_url, count, pn + 1, length)
    return list2


def shangke(club_sk_url, count, pn=1, length=0):
    sk_selector = get_x_selectoro(club_sk_url, pn)
    sk_info = sk_selector.xpath('//div[@class="divHeight"]/table[@cellpadding="0"]/tr/td[7]/text()')
    count = get_useful_time(sk_info, count)
    flag = next_page_flag(club_sk_url)
    length += len(sk_info)
    list2 = [length, count]
    if flag and pn != 2:
        return shangke(club_sk_url, count, pn + 1, length)
    return list2


def pingshishuaka_1(stsuzhi_sk_url, count, pn=1, length=0):
    sttz_selector = get_x_selectoro(stsuzhi_sk_url, pn)
    sttz_info = sttz_selector.xpath('//div[@class="divHeight"]/table[@cellpadding="0"]/tr/td[7]/text()')
    count = get_useful_time(sttz_info, count)
    flag = next_page_flag(stsuzhi_sk_url)
    length += len(sttz_info)
    list2 = [length, count]
    if flag and pn != 2:
        return pingshishuaka_1(stsuzhi_sk_url, count, pn + 1, length)
    return list2


def pingshishuaka_2(zizhuxuexi_sk_url, count, pn=1, length=0):
    zzxx_selector = get_x_selectoro(zizhuxuexi_sk_url, pn)
    zzxx_info = zzxx_selector.xpath('//div[@class="divHeight"]/table[@cellpadding="0"]/tr/td[7]/text()')
    count = get_useful_time(zzxx_info, count)
    flag = next_page_flag(zizhuxuexi_sk_url)
    length += len(zzxx_info)
    list2 = [length, count]
    if flag and pn != 2:
        return pingshishuaka_2(zizhuxuexi_sk_url, count, pn + 1, length)
    return list2


def show_detail(urls, pn=1, all_info=[]):
    selectors = get_x_selectoro(urls, pn)
    infos = selectors.xpath('//div[@class="divHeight"]/table[@cellpadding="0"]/tr/td/text()')
    line_info = []
    if pn == 1:
        all_info = []
    flag = next_page_flag(urls)
    for i in range(len(infos)):
        temp = infos[i]
        s = get_real(temp)
        if s:
            line_info.append(s)
        if s == u"有效" or s == u"有效 ":
            all_info.append(line_info)
            line_info = []
    if flag and pn != 2:
        show_detail(urls, pn+1, all_info)
    return all_info


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

# next_page_flag()