from selenium import webdriver

# 配置浏览器驱动的路径
driver_path = './driver/mac64/chromedriver' 

# https://sites.google.com/chromium.org/driver/?pli=1

# 创建浏览器驱动对象
driver = webdriver.Chrome(driver_path)

# 打开网页
# url = 'http://www.qstheory.cn/qswp.htm'
url = 'http://www.chinadaily.com.cn/'
driver.get(url)

# 等待页面加载完成（可选）
driver.implicitly_wait(1000)

# 获取页面源代码
page_source = driver.page_source

# 关闭浏览器驱动
# driver.quit()

# 处理页面源代码，提取需要的内容
# 示例：输出页面源代码
print(page_source)
