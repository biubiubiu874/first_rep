
from selenium import webdriver

import time
import datetime

driver  = webdriver.Chrome()
driver.get("https://www.12306.cn/index/")
driver.maximize_window()

time.sleep(3)
fromStation = '广州'   #出发地汉字
fs = 'GZQ'   # 出发地代码
ele_fromStation = driver.find_element_by_id("fromStationText")
ele_fs = driver.find_element_by_id("fromStation")

fromStation_js = """
arguments[0].value=arguments[1]
var from = arguments[2]
from.className ="input inp-txt_select";
from.value = arguments[3]
"""
driver.execute_script(fromStation_js, ele_fs, fs, ele_fromStation, fromStation)

time.sleep(3)
toStation = '上海'    # 出发地汉字
ts = 'SHH'  # 出发地代码
ele_toStation = driver.find_element_by_id("toStationText")
ele_ts = driver.find_element_by_id("toStation")

toStation_js = """
arguments[0].value=arguments[1];
var to = arguments[2];
to.className = "input inp-txt_select";
to.value = arguments[3];
"""
driver.execute_script(toStation_js, ele_ts, ts, ele_toStation, toStation)

#定位日期框
date_data = driver.find_element_by_xpath("//*[@id='train_date']")
# now_time = time.strftime('%Y-%m-%d', time.localtime()) # 获取当前时间


now = datetime.datetime.now()
tenday_la=str(now-datetime.timedelta(days=-5))[:10]


driver.execute_script(
    "var a = arguments[0];"
    "a.readOnly=false;"
    "a.value= arguments[1];",date_data,tenday_la)  #执行js语句

time.sleep(3)
check = driver.find_element_by_xpath("//*[@id='search_one']")
check.click()