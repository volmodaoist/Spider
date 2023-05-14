from config import *
from crawler.weibo import for_weibo
from crawler.douban import for_douban


"""

测试豆瓣爬取电影评论的模块
    python main.py --type douban --entry-id 35209731 --st 1 --ed 20
    python main.py --type douban --entry-id 35209733 --st 1 --ed 20
"""
if __name__ == '__main__':
    if args["type"] == "weibo":
        for_weibo()
    if args["type"] == "douban":
        for_douban()