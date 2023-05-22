import requests
import pandas as pd

from config import *
from bs4 import BeautifulSoup


"""
测试样例: 
    entry_id = 35209733, 35209731, 
测试命令:
    python douban.py --entry-id 35209733 --st 1 --ed 20
    python douban.py --entry-id 35209731 --st 1 --ed 20
"""
entry_id = args["entry_id"]
headers = {
    'User-Agent': random.choice(user_agents)
}

def for_douban():
    comments = []
    for i in range(args["st"], args["ed"], 20): # 豆瓣评分每页展示二十条
        url = f'https://movie.douban.com/subject/{entry_id}/comments?start=' + str(i) + '&limit=20&status=P&sort=new_score'
        res = requests.get(url, headers = headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        comment_items = soup.find_all(class_='comment-item')
        for item in comment_items:
            # 豆瓣可能存在一些不打分的评论，因而rating这个键可能返回 None
            # 如果存在用户打分，那么包含分值的元素将是 <span class="allstar40 rating" title="推荐"></span> 
            rating = item.find(class_='rating')
            if rating is not None:
                allstar = rating.get('class')[0]                # 通过class 获取的是一个列表 ["allstar40", "rating"]
                allstar = re.findall(r'\d+$', allstar)[0][0]    # 通过正则表达式提取末尾的数字部分
    
            content = item.find(class_='comment-content').text.strip()
            useful = item.find(class_='votes').text
            comments.append((allstar, content, useful))

    df = pd.DataFrame(comments, 
                      columns = ["用户打分", "评论内容", "点赞数"])
    df.to_csv(f'./data/douban_comments_{entry_id}.csv', 
            index = False,
            encoding = "utf-8-sig")
    