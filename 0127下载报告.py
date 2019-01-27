
# coding: utf-8
import pandas as pd
import requests, os, time

from Proxy import *

proxies = get_proxy()

dfDownload = pd.read_csv(r"./0121/dfDownload.csv", encoding="gbk")

def downloadReport(i, remove=False):
    '''
    用于下载2017年企业社会责任报告，下载格式为 pdf，传入参数为第 i 条企业
    '''
    filename = r"./pdf/{}{}.pdf".format(dfDownload["code"].iloc[i], dfDownload["title"].iloc[i])
    if os.path.exists(filename): 
        if remove:
            os.remove(filename)
            print("{} removed".format(filename))
        else:
            print("{} exists".format(filename))
            return None
    response = getWeb(dfDownload["reportDownload"].iloc[i], proxies=proxies, Return="",
                        sleep=True, sleepMultiply=3)
    with open(filename, "wb") as f:
        f.write(response.content)
    print("{} 成功获取".format(filename))
    return response


from multiprocessing import Pool

pool = Pool()
res = pool.imap_unordered(downloadReport, range(dfDownload.shape[0]))
resultPDF = [item for item in res]
pool.close()

