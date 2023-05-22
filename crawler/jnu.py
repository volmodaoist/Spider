import requests
import pandas as pd
import smtplib

from config import *
from bs4 import BeautifulSoup

# 解析链接
from urllib.parse import urljoin
from urllib.parse import urlparse
from texttable import Texttable
from email.mime.text import MIMEText


# 定义要爬取的网页链接
url = 'https://gs.jnu.edu.cn/tzgg/list1.htm'

# 下面这个函数仍然存在一些问题
def send_qq_email(df, sender_email, sender_password, receiver_email):
    # 邮件相关配置, 其中 SSL/TLS 端口为 465，非加密端口为 587。
    smtp_host = 'smtp.qq.com'
    smtp_port = 465
    
    table = df.to_string(index=False)

    # 创建邮件内容
    message = MIMEText(table, 'plain')
    message['Subject'] = 'Pandas DataFrame Table'
    message['From'] = sender_email
    message['To'] = receiver_email

    with smtplib.SMTP_SSL(smtp_host, smtp_port) as server:
            server.connect(smtp_host, smtp_port)
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            server.quit() # 关闭SMTP连接
    print("Successful send email!")


def for_JNU():
    previous_data = None
    headers = {
        'User-Agent': random.choice(user_agents)
    }
    while True:
        # 发送 GET 请求获取网页内容
        res = requests.get(url, headers = headers)

        # 解析网页内容
        soup = BeautifulSoup(res.content, 'html.parser', from_encoding = 'utf-8')

        # 获取无标签列表 ul.common-list 中的所有 li 元素
        li_elements = soup.select('ul.common-list li')

        # 用于存储本次爬取结果的列表
        current_data = []

        # 提取每个 li 元素中的标题、链接和日期
        for li in li_elements:
            title, date = li.a.text, li.span.text
            link = li.a.get('href')
            
            # 如果获取的链接是一个相对链接，将其转为绝对链接再存储
            is_relative = not bool(urlparse(link).netloc)
            if is_relative:
                link = urljoin(url, link)

            current_data.append([title, link, date])

        # 将本次爬取结果转换为 DataFrame
        df = pd.DataFrame(current_data, columns = ['标题', '链接', '日期'])

        # 如果与上一次爬取结果不一致，则打印 "更新"
        if previous_data is None or not previous_data.equals(df):
            print("This page has been updated...")
            # send_qq_email(df)
            # 保存本次爬取结果为 CSV 文件
            df.to_csv('./data/jnu_news.csv', 
                    index = False, 
                    encoding = "utf-8-sig")

        # 再将本次爬取结果设置为上一次爬取结果
        previous_data = df

        # 暂停一段时间，等待下次爬取
        if not args["dead_loop"]:
             break
        time.sleep(60)  # 设置刷新间隔，单位为秒