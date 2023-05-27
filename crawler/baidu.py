
import urllib
import requests
import os, re, time, json


from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options

# 用于指定元素的查找方式
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from config import *
from utils.debug import cprint

def split_searching_keyword(key_words, op = 1):
    chinese_comma, chinese_semicolon = '\uFF0C', '\uFF1B'
    if not any(delimiter in key_words for delimiter in [',', chinese_comma, ';', chinese_semicolon]): 
        return f'("{key_words}")'

    key_words_list = []
    if ',' in key_words:
        key_words_list = key_words.split(',')
    elif chinese_comma in key_words:
        key_words_list = key_words.split(chinese_comma)
    elif ';' in key_words:
        key_words_list = key_words.split(';')
    elif chinese_semicolon in key_words:
        key_words_list = key_words.split(chinese_semicolon)

    if op == 0:
        key_words_new = ' + '.join([w.strip() for w in key_words_list])
    elif op == 1: 
        key_words_new = ' | '.join([w.strip() for w in key_words_list[::-1]])

    return f'({key_words_new})'


class BaiduAcademicCrawler:
    def __init__(self, chrome_driver_path = "./driver/mac64/chromedriver") -> None:
        self.chrome_driver_path = chrome_driver_path
        
        options = Options() # 创建驱动选项
        options.add_experimental_option('excludeSwitches', ['enable-automation']) 
        
        # 创建一个 Chrome 浏览器实例，使用指定的 Chrome 驱动程序路径和选项。
        self.browser = webdriver.Chrome(executable_path  = self.chrome_driver_path,
                                        options = options)
        self.browser.implicitly_wait(3)
        self.wait = WebDriverWait(self.browser, 15)

        # 用于执行浏览器操作的动作链
        self.ac = ActionChains(self.browser)
        

    def _wait_by_xpath(self, patten):
        # Expected Conditions 模块，来自于 Selenium，并将其重命名 EC，用于定义等待条件, (By.XPATH, patten) 指定了元素的查找方式为 XPath，patten 是传入的 XPath 表达式!
        self.wait.until(EC.presence_of_element_located((By.XPATH, patten)))

    def is_contain_chinese(self, check_str):
        for ch in check_str:
            if u'\u4e00' <= ch <= u'\u9fff':
                return True
        return False


    def replace_special_char(self, paper_name):
        if ': ' in paper_name:
            paper_name = paper_name.split(': ')[0]
        if '&amp;' in paper_name:
            paper_name = paper_name.replace('&amp;', '&')
        if '&#039;' in paper_name:
            paper_name = paper_name.replace('&#039;', "'")
        return paper_name


    def run(self, wd, page_num = 999, year = 2018, fpath = './data/xpaper_fromBaidu_result.txt', pos = 0):
        headers = {  # 这个之后需要修改
            'user-agent':  random.choice(user_agents),
        }

        all_dic = {
            'all_paper_num': 0,
            'English Journal': {},
            'Chinese Journal': {},
            'Conference': {},
        }

        first_paper = str()
        count, paper_count, conference_count, chinese_count, english_count = 0, 0, 0, 0, 0

        # 定义内部函数
        # 爬取数据jsonify，然后写入磁盘，其中写入函数的 ensure_ascii=False 参数表示允许非阿斯克码字符不经转移输出
        def write_json(data, msg = None):
            if msg is not None:
                print(msg)
            with open(fpath, 'w', encoding = 'utf8') as fw:
                fw.write(json.dumps(data, ensure_ascii = False))
                fw.flush()

        def update_paper_counter(type_key, paper_count, english_count, chinese_count, conference_count):
            all_dic['all_paper_num'] = {
                'all_count': paper_count, 'Conference count': conference_count,
                'English Journal count': english_count, 'Chinese Journal count': chinese_count
            }
            for journal_name in list(all_dic[type_key].keys()):
                journal = all_dic[type_key][journal_name]
                if '共' in journal[0]:
                    journal[0] = f'共 {len(journal)-1} 篇'
                else:
                    journal.insert(0, f"共 1 篇")
            all_dic[type_key] = {key: all_dic[type_key][key] for key, value in
                                        sorted(all_dic[type_key].items(), key=lambda x: x[1][0], reverse = True)}
     

        # 检索位置通过 args 控制，到时候再改
        stop = False
        while count <= page_num and not stop:
            if pos == 0:
                url = f'https://xueshu.baidu.com/s?wd=intitle:{wd}&pn={count}0&tn=SE_baiduxueshu_c1gjeupa&ie=utf-8&filter=sc_year%3D%7B{year}%2C%2B%7D&sc_f_para=sc_tasktype%3D%7BfirstSimpleSearch%7D&bcp=2&sc_hit=1'
            elif pos == 1:
                url = f'https://xueshu.baidu.com/s?wd={wd}&pn={count}0&tn=SE_baiduxueshu_c1gjeupa&ie=utf-8&filter=sc_year%3D%7B{year}%2C%2B%7D&sc_f_para=sc_tasktype%3D%7BfirstAdvancedSearch%7D&bcp=2&sc_hit=1'
        
            url = urllib.request.quote(url, safe =";/?:@&=+$,", encoding = "utf-8")

            try: # 访问一个特定的 URL,如果在访问过程中出现异常，执行异常处理模块
                self.browser.get(url)
            except:
                print(f'Google Chrome has been shut down abnormally.\n') # 浏览器异常终止
                time.sleep(3)
                continue

            print(f'Baidu Scholar Page {count + 1}:  {url}\n')
            time.sleep(1)

            # 软件打开的浏览器在程序运行结束之前请勿人为终止
            search_result_elements = self.browser.find_elements_by_xpath(
                '/html/body/div[1]/div[4]/div[3]/div[2]/div/div[@class="result sc_default_result xpath-log"]')
            
            if search_result_elements is None: # 如果没有搜索结果，提前结束
                write_json(all_dic, "Not further result")
                return

            for i, search_result_element in enumerate(search_result_elements):
                if count == 0 and i == 0:
                   write_json(all_dic)
                else:
                    with open(fpath, 'r', encoding='utf8') as fr:
                        all_dic = json.loads(fr.read())
                
                # 下面三行代码需要保证代码运行期间，谷歌浏览器不被异常终止
                paper_name = search_result_element.find_element_by_xpath('div[1]/h3/a')
                paper_link = paper_name.get_attribute("href")
                paper_name = paper_name.text

                if paper_link == first_paper:
                    stop = True # 用于跳出外层的 while 循环
                    break

                first_paper = paper_link if i == 0 else first_paper

                try:
                    res = requests.get(paper_link, headers = headers).text
                except: # 网络被禁，稍等一段时间再爬取页面的内容
                    print(f'The network is banned, wait a moment to crawl again\n')
                    time.sleep(5)
                    continue

                # 通过正则表达式找出到的符合条件的元素，这些元素会以列表形式返回
                journal_name = re.findall('<a class="journal_title".*?>(.*?)</a>', res, re.S) 
                if not journal_name:
                    continue
                journal_name = journal_name[0]
                journal_name = self.replace_special_char(journal_name)
                paper_count += 1

                print(f'第{paper_count}篇论文')

                if self.is_contain_chinese(journal_name):
                    print(f" Title: {paper_name}\n Link: {paper_link}\n Journal Name: {journal_name}")
                    all_dic['Chinese Journal'].setdefault(journal_name, []).append({paper_name: paper_link})
                    chinese_count += 1
                    update_paper_counter('Chinese Journal', paper_count, english_count, chinese_count, conference_count) # 更新篇目
                    write_json(all_dic)
                    time.sleep(3)
                    continue

                if 'Conference' in journal_name:
                    print(f" Title: {paper_name}\n Link: {paper_link}\n Journal Name: {journal_name}")
                    all_dic['Conference'].setdefault(journal_name, []).append({paper_name: paper_link})
                    conference_count += 1
                    update_paper_counter('Conference', paper_count, english_count, chinese_count, conference_count)      # 更新篇目
                    write_json(all_dic)
                    time.sleep(3)
                    continue

                status_code = True
                cite_score, journal_division, journal_date = '', '', ''

                while status_code:
                    try:
                        post_dic = {'searchname': journal_name, 'searchsort': 'relevance'}
                        search_url = 'http://www.letpub.com.cn/index.php?page=journalapp&view=search'
                        res = requests.post(search_url, post_dic, headers = headers)
                    except:
                        print("The network is banned by letpub, wait a moment to crawl again")
                        time.sleep(5)
                        continue

                    if res.status_code == 200:
                        status_code = False
                    else:
                        print(f"The network is banned by letpub, wait a moment to crawl {journal_name} again")
                        time.sleep(5)
                        continue
                    
                    journal_info = re.findall('</style>.*?<tr>(.*?)</tr>', res.text, re.S)[0]
                    
                    # 获取期刊的引用得分
                    cite_score = re.findall('CiteScore:(\d+.\d+)', journal_info, re.S)
                    
                    # 获取期刊的分区
                    journal_division = re.findall('(\d区)</td>', journal_info, re.S)
                    journal_division = ["SCI-" + i.replace("区","") for i in journal_division]

                    # 获取期刊的审稿日期
                    journal_date = str()
                    search_patterns = ['月', '周', 'eeks']
                    for table_data in re.findall('(<td.*?</td>)', journal_info, re.S):
                        if any(pattern in table_data for pattern in search_patterns):
                            journal_date = re.findall('>(.*?)</td>', table_data, re.S)
                            break

                if cite_score and journal_division and journal_date:
                    journal_name = f'{journal_division[0]} Citescore: {cite_score[0]} 审稿周期: {journal_date[0]} {journal_name}'
                elif cite_score and journal_division:
                    journal_name = f'{journal_division[0]} Citescore: {cite_score[0]} 审稿周期: 无记录 {journal_name}'
                elif cite_score:
                    journal_name = f'None Citescore:{cite_score[0]} 审稿周期: 无记录 {journal_name}'
                else:
                    journal_name = f'None Not-Citescore 审稿周期: 无记录 {journal_name}'
                print(f" Title: {paper_name}\n Link: {paper_link}\n Journal Name: {journal_name}")
                all_dic['English Journal'].setdefault(journal_name, []).append({paper_name: paper_link})
                english_count += 1
                update_paper_counter('English Journal', paper_count, english_count, chinese_count, conference_count)
                write_json(all_dic)
                time.sleep(5)
            count += 1

        print('Finish!')
        return 0
    

def for_baidu(keywords):
    keywords = split_searching_keyword(keywords)
    state_code = BaiduAcademicCrawler().run(keywords)
    return state_code


if __name__ == '__main__':
    keywords = split_searching_keyword("deep learning")
    BaiduAcademicCrawler().run(keywords)
