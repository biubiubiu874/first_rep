from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()

driver.get("http://www.baidu.com")

element = driver.find_element_by_id("kw")   # WebElement对象 - 1个对象对应1个元素
element.send_keys("selenium webdriver")
driver.find_element_by_id('su').click()  # 带来了内容上的变化


# js当中，将元素拖动到可视区域的js语句。
# 如何确认在当前网页当中，是否需要将元素拖动到可视区域？

# loc = (By.XPATH,'//div[@id="page"]//span[text()="2"]')
loc = (By.XPATH,'//a[text()=" 常用API - Ethon - 博客园"]')
WebDriverWait(driver,10).until(EC.visibility_of_element_located(loc))
a = driver.find_element(*loc)

# # js函数 - 元素对象.scrollIntoView();
# driver.execute_script('arguments[0].scrollIntoView(false);',a)  # arguments 接收外部参数。列表。
# # a.click()

# 滚动到页面底部
driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
time.sleep(2)

# 滚动到页面顶部
driver.execute_script("window.scrollTo(document.body.scrollHeight,0)")


