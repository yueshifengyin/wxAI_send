'''
这是一个简单的爬虫脚本，从中国天气网获取指定城市天气
name：包子
date：2018.10.22
'''

import requests
import random
import time
import socket
import http.client
from bs4 import BeautifulSoup
from setting import *

def weather():
    #  获取每个城市对应天气的url
    def get_url(city_name):
        url = 'http://www.weather.com.cn/weather/'
        with open(r'C:\Users\gaoyue\Desktop\项目\wxAI\city.txt', 'r', encoding='UTF-8') as fs:
            lines = fs.readlines()
            for line in lines:
                if (city_name in line):
                    code = line.split('=')[0].strip()
                    return url + code + '.shtml'
        raise ValueError('invalid city name')

    #  对网页获取get请求，得到的是response对象
    def get_content(url, data=None):
        #  模拟浏览器访问
        header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.235'
        }
        #  超时，取随机数是因为防止被网站认定为网络爬虫
        timeout = random.choice(range(80, 180))
        while True:
            try:
                #  获取请求数据
                rep = requests.get(url, headers=header, timeout=timeout)
                rep.encoding = 'utf-8'
                # print(rep)
                break
            except socket.timeout as e:
                print('3:', e)
                time.sleep(random.choice(range(8, 15)))
            except socket.error as e:
                print('4:', e)
                time.sleep(random.choice(range(20, 60)))
            except http.client.BadStatusLine as e:
                print('5:', e)
                time.sleep(random.choice(range(30, 80)))
            except http.client.BadStatusLine as e:
                print('6:', e)
                time.sleep(random.choice(range(5, 15)))

        return rep.text

    # 获取html中我们所需要的字段：
    def get_data(html_text, city_name):
        #  final元组存放七天的数据
        final = []
        t = []
        t.append(city_name)
        final.append(t)
        bs = BeautifulSoup(html_text, "html.parser")  # 创建BeautifulSoup对象，解析器为：html.parser
        body1 = bs.body  # 获取body部分

        # print(body1)
        data = body1.find('div', {'id': '7d'})  # 找到id为7d的div
        ul = data.find('ul')  # 获取ul部分
        li = ul.find_all('li')  # 获取所有的li

        for day in li:  # 对每个li标签中的内容进行遍历
            # temp代存每日的数据
            temp = []
            #  添加日期
            data = day.find('h1').string  # 找到日期
            temp.append(data)  # 添加到temp中

            inf = day.find_all('p')  # 找到li中的所有p标签
            #  添加天气状况
            temp.append(inf[0].string)  # 第一个p标签中的内容（天气状况）加到temp中
            #  添加最高气温
            if inf[1].find('span') is None:
                temperature_highest = None  # 天气当中可能没有最高气温（傍晚）
            else:
                temperature_highest = inf[1].find('span').string  # 找到最高气温
                temperature_highest = temperature_highest.replace('℃', '')
            temp.append(temperature_highest)  # 将最高温添加进去
            # 添加最低气温
            temperature_lowest = inf[1].find('i').string  # 找到最低温
            temperature_lowest = temperature_lowest.replace('℃', '')  # 最低温度后面有个℃，去掉这个符号
            temp.append(temperature_lowest)  # 将最低温添加上去

            final.append(temp)  # 将temp 加到final中

        return final

    # url = get_url(city)  # 获取城市天气的url
    # print(url)
    html = get_content(url)
    # print(html)# 获取网页html
    result = get_data(html, city)  # 爬去城市的信息
    return result


if __name__ == '__main__':
    result = weather()
    print(city,result)

# https://blog.csdn.net/heshushun/article/details/77772408