from selenium import webdriver
from selenium.webdriver.chrome.options import Options

"""
下面是一些测试样例，可以尝试打开下面的网页
    url = 'http://www.qstheory.cn/qswp.htm'
    url = 'http://www.chinadaily.com.cn'
"""


# 需要用户根据自己的浏览器版本号去配置浏览器驱动的路径
def simulate_WebBrowser(url, time_delay = 100, driver_path = './driver/mac64/chromedriver'):
    """
    :param url: 网页链接 
    :param driver_path: 驱动路径 具体驱动版本需要根据自己电脑的浏览器版本下载，下载链接: https://sites.google.com/chromium.org/driver/?pli=1
                        另外，这个 simulate_WebBrowser 函数模块是由 main.py 文件调用的，因而其默然参数的路径是相对于 main.py 所在的目录来说的
    """
    
    # 通过设置 Options 对象来启用无头浏览器模式，并且禁用 GPU 加速。这样就可以在后台执行网页操作，而不会弹出浏览器窗口。
    options = Options()
    options.add_argument('--headless')     # 启用无头浏览器模式
    options.add_argument('--disable-gpu')  # 禁用 GPU 加速

    driver = webdriver.Chrome(driver_path, options=options)  # 创建浏览器驱动对象
    driver.get(url)  # 使用浏览器进程打开一个 url

    # 等待页面加载完成（可选）
    driver.implicitly_wait(time_delay)

    # 获取页面源代码
    page_source = driver.page_source

    # 关闭浏览器驱动
    driver.quit()

    # 返回页面源代码，用户提取需要的内容
    return page_source
