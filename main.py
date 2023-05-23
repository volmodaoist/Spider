from config import *
from crawler.jnu import for_JNU
from crawler.weibo import for_weibo
from crawler.douban import for_douban

from utils.simulate import simulate_WebBrowser

"""
测试豆瓣爬取电影评论的模块
    python main.py --type douban --entry-id 35209731 --st 1 --ed 20
    python main.py --type douban --entry-id 35209733 --st 1 --ed 20

测试 JNU 通知通告爬取模块
    python main.py --type jnu         
"""
if __name__ == '__main__':
    print(simulate_WebBrowser("http://www.qstheory.cn/qswp.htm"))
    if args["type"] == "weibo":
        for_weibo()
    elif args["type"] == "douban":
        for_douban()
    elif args["type"] == "jnu":
        for_JNU()
    