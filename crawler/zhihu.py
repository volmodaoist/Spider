from config import *

import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from bs4 import BeautifulSoup
from tqdm import tqdm

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

author_id = args["author_id"]

headers = {
    'User-Agent': random.choice(user_agents)
}

chrome_options = Options()
chrome_options.add_argument("--headless")  # 无界面模式
chrome_options.add_argument("--disable-gpu")
driver = webdriver.Chrome(f"user-agent={random.choice(user_agents)}")

def scrape_zhihu_user_articles(page):
    # 构造用户主页的URL
    user_url = f"https://www.zhihu.com/people/{author_id}/posts"+ f"?page={page}"
    

     # 发送HTTP请求，获取用户主页的内容
    try:
        driver.get(user_url)
        html = driver.page_source

        #response = requests.get(user_url.format(page), headers=headers, verify=False, timeout=10,proxies=None)
        
        #response.raise_for_status()
        #html = response.text

        # 使用BeautifulSoup解析HTML代码
        soup = BeautifulSoup(html, 'html.parser')

        # 查找所有文章项
        articles = soup.find_all('div', class_='List-item')

        # 遍历每篇文章，提取信息并打印
        for article in articles:
            like_count = article.find('button', class_='Button VoteButton VoteButton--up').find('span').get("aria-label")
            print("点赞数:", like_count)
            print("--------------------")
            
    except requests.exceptions.RequestException as e:
        print("请求发生错误:", e)


    # 遍历每篇文章，提取信息并打印
    #for article in articles:
        # 提取文章日期
        #article_date = article.find('span', class_='ContentItem-time').get_text().strip()
        
        # 提取文章标题
        #article_title = article.find('h2').get_text().strip()
        
        # 提取文章点赞数和评论数
        #like_count = article.find('button', class_='Button VoteButton VoteButton--up').find('span').get("aria-label")
        #comment_count = article.find('a', class_='Button ContentItem-action Button--plain Button--withIcon Button--withLabel').find('span').get_text().strip()
        
        # 打印文章信息
        #print("日期:", article_date)
        #print("标题:", article_title)
        #print("点赞数:", like_count)
        #print("评论数:", comment_count)
        #print("--------------------")

def for_zhihu():
     #zhihu_data = []
     for page in tqdm(range(args["st"], args["ed"])):  
        #zhihu_data += scrape_zhihu_user_articles(page)
        scrape_zhihu_user_articles(page)

driver.quit()