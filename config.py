"""
这是一个配置文件，主要包括三个部分:
    1. 导入Python模块
    2. 自定义一个参数解析器
    3. 存储代理池等全局常量
"""

import requests
import pandas as pd
import pytz
import random
import datetime
import os, sys, re, time
import argparse


# 自定义的参数解析器
parser = argparse.ArgumentParser(description = 'parsing the command-line arguments')

# 爬虫抓取的用户平台
parser.add_argument('-t', '--type', 
    choices = ['weibo', 'douban', 'jnu', 'zhihu', 'bilibili', 'news'], 
    help = 'Choose a type of social media platform')
# 爬虫抓取的用户id，适用于微博
parser.add_argument('--user-id', type = str,
    help = "Enter the user id you want to scrape")
# 爬虫抓取的作业id，适用于豆瓣的作品评分
parser.add_argument('--entry-id', type = str,
    help = "Enter the entry id you want to scrape")
# 爬虫抓取的作者id，适用于知乎
parser.add_argument('--author-id', type = str,
    help = "Enter the author id you want to scrape")
# 爬虫抓取的网页链接
parser.add_argument('--url', type = str,
    help = "URL to web page crawled by the crawler")
# 爬虫抓取的起始页面
parser.add_argument('--st', type = int, default = 1,
    help = "Crawler start page")  
# 爬虫抓取的结束页面
parser.add_argument('--ed', type = int, default = 100,
    help = "Crawler end page")
# 爬虫抓取的起始年份
parser.add_argument('--st_year', type = int, default = 2018,
    help = "Crawler start year")
# 爬虫抓取的结束年份
parser.add_argument('--ed_year', type = int, default = 2022,
    help = "Crawler end year")
parser.add_argument("--dead-loop", type = bool, default = False,
    help = "Real-time updates through endless loop control")

args = vars(parser.parse_args())



# 使用一个代理池，随机选择一个User-Agent来进行请求
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
  
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0)\
    Gecko/20100101 Firefox/105.0",
  
  	"Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
  	AppleWebKit/537.36 (KHTML, like Gecko)\
    Chrome/89.0.4389.82 Safari/537.36 Edg/89.0.774.45",
  
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",
  
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0)\
    Gecko/20100101 Firefox/88.0",

    "User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
]


