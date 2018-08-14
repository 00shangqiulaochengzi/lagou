# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 19:52:09 2018

@author: chenyan
"""

from urllib import request,parse
import random
import re
import time
import json

# 设置UA池，每次随机从池中取一个userAgent
def get_UA():
    l = ["Mozilla/5.0 (iPhone; CPU iPhone OS 9_2 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) CriOS/47.0.2526.70 Mobile/13C71 Safari/601.1.46",
         "Mozilla/5.0 (Linux; U; Android 4.4.4; Nexus 5 Build/KTU84P) AppleWebkit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
         "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0)"]
    return random.choice(l)

def web_info(url, minPageNum, maxPageNum):
    # 设置headers信息
    headers = {
               'Cookie':'Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1533216476; _ga=GA1.2.2013844225.1533216476; _gat=1; user_trace_token=20180802212758-deece69b-9657-11e8-a0db-5254005c3644; LGSID=20180802212758-deece9ce-9657-11e8-a0db-5254005c3644; PRE_UTM=m_cf_cpt_360_pc; PRE_HOST=www.so.com; PRE_SITE=https%3A%2F%2Fwww.so.com%2Fs%3Fie%3Dutf-8%26src%3D360chrome_toolbar_search%26q%3D%25E6%258B%2589%25E5%258B%25BE%25E7%25BD%2591; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Flp%2Fhtml%2Fcommon.html%3Futm_source%3Dm_cf_cpt_360_pc; LGUID=20180802212758-deecec95-9657-11e8-a0db-5254005c3644; X_HTTP_TOKEN=02ea614f7cc9972ec49d976dca7bf78d; LG_LOGIN_USER_ID=39ecd4c98b4867e099a6bb0f2fb0f9c06616e638c3965cbee04b0adcec7994d1; _putrc=238B2D799A902A58123F89F2B170EADC; login=true; unick=%E9%99%88%E5%86%B0%E8%A8%80; gate_login_token=9444690a66f0502f168a96b6a1bdc0942efa06a8280f384eec5321ea5abacd67; JSESSIONID=ABAAABAAAFDABFGBE91F7EB5B87446DFC4110B673B81DBD; _ga=GA1.3.2013844225.1533216476; _gid=GA1.2.1268074258.1533216498; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1533216541; LGRID=20180802212903-05bb9207-9658-11e8-a0db-5254005c3644',
               'Host': 'm.lagou.com',
               'Referer':'https://m.lagou.com/search.html',
               'User-Agent': get_UA()
               }
    
    # 用GET方法向服务器发送请求
    for pageNo in range(minPageNum, maxPageNum):
        params = {'city': '全国',
                  'positionName':'web',
                  'pageNo':pageNo,
                  'pageSize':'15'}
        
        # 对要提交的数据做一次urlencode
        params = parse.urlencode(params)
        full_url = url + params
        
        # 向服务器发送请求
        req = request.Request(full_url, headers=headers)
        response = request.urlopen(req)
        position_messages = response.read().decode('utf-8')
        
        # 使用正则表达式提取数据
        pattern = re.compile("""positionName":"([\s\S]*?)","city":"([\s\S]*?)"[\s\S]*?"createTime":"([\s\S]*?)","salary":"([\s\S]*?)"[\s\S]*?.png","companyName":"([\s\S]*?)","companyFullName":"([\s\S]*?)"}""")
        items = re.findall(pattern, position_messages)
        
        for item in items:
            item = {
                    '职位': item[0].strip(),
                    '地址': item[1].strip(),
                    '时间': item[2].strip(),
                    '薪资': item[3].strip(),
                    '公司名称': item[4].strip(),
                    '公司全称': item[5].strip()
                    }
            write_to_file(item)
            
# 保存到本地文件系统中
def write_to_file(item):
    # 存储成json格式，以便于将来能方便的提取出来
    with open("lagou.csv", 'a', encoding="utf-8") as f:
        f.write(json.dumps(item, ensure_ascii=False)+'\n')   

if __name__ == '__main__':
    minPageNum = 1
    maxPageNum = 31
    url = 'https://m.lagou.com/search.json?'
    position_messages = web_info(url, minPageNum, maxPageNum)
    
    
    
    
    
    
    