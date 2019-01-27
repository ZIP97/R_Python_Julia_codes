# -- utf-8 --
import requests 
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
# import re, os
import numpy as np
import time

def get_proxy():
    '''
    用于从 http://www.xicidaili.com/nn 获取代理
    返回 代理列表(100个元素)
    '''
    # 报头设置
    def header(website):
        #ua = UserAgent()
        #web = requests.get(website, headers={'user-agent': ua.random})
        web = requests.get(website, headers={'user-agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"})

        text = web.text
        return text
    # 解析代理
    def parse_proxy(*data):
        temp = [item for iitem in data for item in iitem] # data 两个参数
        a = np.array([item.get_text() for iitem in temp for item in iitem.find_all("td")])
        ip = a[range(1, 500*2, 10)]
        port = a[range(2, 500*2, 10)]
        typ = map(np.str.lower, a[range(5, 500*2, 10)])
        return ip, port, list(typ)
    # 读取网页
    proxy_api = 'http://www.xicidaili.com/nn'
    data = header(proxy_api)#.decode('utf-8')
    data_soup = BeautifulSoup(data, 'lxml')
    data_odd = data_soup.select('.odd')
    data_ = data_soup.select('.')
    # 解析代理网址 获取ip池（100个）
    ip, port, typ = parse_proxy(data_odd, data_)
    proxies = map(lambda a, b, c: a+"://"+b+":"+c, typ, ip, port)
    print("成功获取代理！")
    return list(proxies)


def gen_proxy(proxies):
    '''
    用于 requests 代理参数设置： proxies = gen_proxy(proxies)
    :param proxies: 代理列表
    返回 dict ，例如 {'http': 'http://180.213.180.149:53281'}
    '''
    a = proxies[np.random.randint(5, 90)]
    return {a[:a.find(":")]: a}

def get_ele_class(soup, s, more=False):
    '''
    解析带 class 的 soup
    :param s: 类似 'p class="abc"'，但 class 的值必须无空格
    '''
    s1, s2 = s.split()
    if not more: return soup.find(s1, class_=s2[s2.find("=")+2:-1]).get_text().strip()
    else: return [item.get_text().strip() for item in soup.find_all(s1, class_=s2[s2.find("=")+2:-1])]
    
    
def get_call(call, Return="soup", Max=10):
    '''
    获取网页：防止因为代理或者暂时的服务器问题导致网页不可获取。
    :param call: requests.get() 或者 requests.post()
    :param Return: 可选参数 "soup" "json" "text" "status"
    '''
    cond = True
    i = 0
    while cond:
        i = i+1
        try: response = call; cond = response.status_code!=200
        except: pass #cond = True
        if i == Max: print("网页获取失败！"); return None # 若网页获取失败，则返回 None
    if Return == "soup": return BeautifulSoup(response.text)
    elif Return == "json": return response.json()
    elif Return == "text": return response.text
    elif Return == "content": return response.content.decode("utf8")
    elif Return == "status": return response.status_code, i
    
#def getWeb(url, Return, proxies, timeout=1, Max=20):
#     '''
#     用于排除无效代理，并成功获得网页：排除触发 ProxyError 的代理；或者链接超时的代理
#     :param url: get 获取的网址
#     :param Return: 可选参数 "soup" "json" "text" "status" "proxy"
#     :param timeout: 超时时间设置，单位 秒
#     :param Max: 失败次数设置，达到 Max 次则返回 None
#     '''
#     proxy = gen_proxy(proxies)
#     a = True
#     i = 0
#     while a:
#         i += 1
#         try: response = requests.get(url, proxies=proxy, timeout=timeout, headers={'user-agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}); a = response.status_code!=200; print("第{}次代理成功".format(i))
#         except requests.exceptions.ProxyError: proxy = gen_proxy(proxies); print("代理失败")
#         except requests.exceptions.Timeout: proxy = gen_proxy(proxies); print("代理超时")
#         if i == max: return None
#     if Return == "soup": return BeautifulSoup(response.text, "lxml")
#     elif Return == "json": return response.json()
#     elif Return == "text": return response.text
#     elif Return == "content": return response.content.decode("utf8")
#     elif Return == "status": return response.status_code, i
#     elif Return == "proxy": return proxy
    
def getWeb(url, Return, proxies, imitate=False, cookies=None, timeout=1, Max=20, sleep=False):
    '''
    用于排除无效代理，并成功获得网页：排除触发 ProxyError 的代理；或者链接超时的代理
    :param url: get 获取的网址
    :param Return: 可选参数 "soup" "json" "text" "status" "proxy"
    :param timeout: 超时时间设置，单位 秒
    :param Max: 失败次数设置，达到 Max 次则返回 None
    :param imitate: 是否模拟登录
    :param cookies: 模拟登录时需提供 cookies 内容
    '''
    loop, i = True, 0
    while loop:
        i += 1
        proxy = gen_proxy(proxies)
        if not imitate:
            try: response = requests.get(url, proxies=proxy, timeout=timeout, headers={'user-agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}); loop = response.status_code!=200; print("第{}次代理成功".format(i))
            except requests.exceptions.ProxyError: proxy = gen_proxy(proxies); print("代理失败")
            except requests.exceptions.Timeout: proxy = gen_proxy(proxies); print("代理超时")
            if i == Max: return None
        else:
            headers = {
                'Origin': 'http://58921.com',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
                'Referer': 'http://58921.com/user/login',
                'X-Requested-With': 'XMLHttpRequest',
                'Connection': 'keep-alive',
                'DNT': '1',
            }
            params = (
                ('ajax', 'submit'),
                ('__q', 'user/login'),
            )
            data = {
              'mail': '1137967378@qq.com',
              'pass': '1137967378',
              'form_id': 'user_login_form',
              'form_token': '5b2d65d8ff0011b40c89930cea15f4f7',
              'submit': '\u767B\u5F55'
            }
            url_login = 'http://58921.com/user/login/ajax'
            try:
                s = requests.Session()
                response = s.post(url_login, headers=headers, params=params, cookies=cookies, 
                                  data=data, proxies=proxy, timeout=timeout)
                if sleep: time.sleep(np.random.rand())
                response = s.get(url, proxies=proxy, timeout=timeout)
                s.close(); loop = False; print("第{}次代理成功".format(i))
            except requests.exceptions.ProxyError: proxy = gen_proxy(proxies); print("代理失败")
            except requests.exceptions.Timeout: proxy = gen_proxy(proxies); print("代理超时")
    if Return == "soup": return BeautifulSoup(response.text, "lxml")
    elif Return == "json": return response.json()
    elif Return == "text": return response.text
    elif Return == "content": return response.content.decode("utf8")
    elif Return == "status": return response.status_code, i
    elif Return == "proxy": return proxy
    

def get_start_end_date(releaseDate, delta, sep=False):
    '''
    时间转换：给定上映日期和前后间隔天数，计算开始日期和结束日期。
    若间隔0天，则将发行日期转化成带有 '-' 的发行日期。
    默认所有参数日期格式为8位年月日日期。
    '''
    if not delta==0:
        releaseDate = pd.Timestamp(releaseDate)
        timedelta = pd.Timedelta("{} days".format(delta))
        startDate = releaseDate-timedelta
        endDate = releaseDate+timedelta
        if sep: startDate, endDate = str(startDate).split()[0], str(endDate).split()[0]
        else: startDate, endDate = str(startDate).split()[0].replace("-", ""), str(endDate).split()[0].replace("-", "")
        return startDate, endDate
    else: return "-".join([releaseDate[:4], releaseDate[4:6], releaseDate[6:8]])
