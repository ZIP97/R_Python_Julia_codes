# coding: utf-8
import numpy as np
import pandas as pd
import requests, os
from bs4 import BeautifulSoup
from multiprocessing import Pool
from Proxy import get_proxy, getWeb, gen_proxy
proxies = get_proxy()

def get_write(i):
    '''
    获取每年年报，并写入 txt 文件
    :param i: 年度报告列表第几个年报
    '''
    text = getWeb(df.href.iloc[i], Return="text", proxies=proxies)
    text = text.replace("&ensp;", "")
    # text = text.replace("\r<br/>", "")
    txtFile = r"{}{}_{}.txt".format(txtPath, code, df["公告标题"].iloc[i])
    with open(txtFile, "w") as f:
        f.write(text)
    return text

txtPath = "./txt/"
csvPath = "./年度报告/"

code = "601899"
corp = "紫金矿业"
# 解析 网易财经 定期报告表格，获取年报链接
url = "http://quotes.money.163.com/f10/gsgg_{},dqbg.html".format(code)
soupTable = getWeb(url, proxies=proxies, Return="soup")
result = soupTable.find_all("div", class_="tabs_panel")
res = result[0].get_text().split("\n")
res = list(filter(None, res))[:-1]
href = ["http://quotes.money.163.com"+item.get("href") for item in result[0].find_all("a")][:-3]
npRes = np.array(res).reshape(-1, 3)
df = pd.DataFrame(npRes[1:, :], columns=npRes[0, :])
df["href"] = href
df["releaseYear"] = df["公布日期"].map(lambda x: x[:4])
index = df["公告类型"]=="年度报告"
df = df[index]
df.to_csv("{}{}_{}.csv".format(csvPath, code, corp), encoding="gbk", index=False)

# 多进程获取网页数据并保存
pool = Pool()
temp = pool.imap_unordered(get_write, range(len(df)))
texts = [item for item in temp]
pool.close()


