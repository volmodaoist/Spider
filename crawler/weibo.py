from config import *
from tqdm import tqdm
from bs4 import BeautifulSoup


""" 测试样例: 
2714280233  papi酱
1792634467  珀莱雅PROYA
"""

user_id = args["user_id"]
url = f"https://m.weibo.cn/api/container/getIndex?\
        uid={user_id}\
        &type=uid\
        &value={user_id}\
        &containerid=107603{user_id}" + "&page={}"

def get_weibo_data(page):
    headers = {
        "User-Agent": random.choice(user_agents),
        "Referer": f"https://m.weibo.cn/u/{user_id}",
        "X-Requested-With": "XMLHttpRequest",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Cache-Control": "max-age=0",
        "TE": "Trailers"
    }
    res = requests.get(url.format(page), headers = headers)
    json_data = res.json()
    cards = json_data["data"]["cards"]
    weibo_data = []
    
    # 增加时间限定，只看 2018-2022
    start_date = datetime.datetime(args["st_year"], 1, 1)
    end_date = datetime.datetime(args["ed_year"], 12, 31)
   
    tz = pytz.timezone('Asia/Shanghai')
    start_date = tz.localize(start_date)
    end_date = tz.localize(end_date)

    for card in cards:
        if card.get("mblog"):
            mblog = card["mblog"]
            created_at = datetime.datetime.strptime(mblog["created_at"], "%a %b %d %H:%M:%S %z %Y")
            if start_date <= created_at <= end_date:
                text = BeautifulSoup(mblog["text"], features="html.parser").get_text()
                like_count = mblog["attitudes_count"]
                reposts_count = mblog["reposts_count"]
                comments_count = mblog["comments_count"]
                created_date = created_at.strftime('%Y-%m-%d')
                weibo_data.append((created_date, text, like_count, comments_count, reposts_count))

    # 每爬取一页之后随机暂停一段时间，避免访问过于频繁
    time.sleep(1 * random.random())
    
    return weibo_data


# 爬取[bg, ed]页面区间的微博数据
def for_weibo():
    weibo_data = []
    for page in tqdm(range(args["st"], args["ed"])):  
        weibo_data += get_weibo_data(page)

    # 转换成Pandas DataFrame并输出为 csv
    df = pd.DataFrame(weibo_data, 
                      columns = ["发布时间", "微博内容", "点赞数", "评论数", "转发数"])
    df.to_csv(f"./data/weibo_data_{user_id}.csv", 
            index = False, 
            encoding = "utf-8-sig")
