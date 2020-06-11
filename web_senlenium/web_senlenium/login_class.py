# -*- coding:utf-8 -*-
# _author_='lijiachang'
# @time :2020/3/4 18:32
from selenium import webdriver
import time
from selenium.webdriver.support.wait import WebDriverWait

#打开腾讯课堂
drive = webdriver.Chrome()
drive.implicitly_wait(5)
drive.get("https://ke.qq.com/")
drive.maximize_window()

#找到登陆，点击
drive.find_element_by_id("js_login").click()
drive.find_element_by_xpath('//a[@href="javascript:void(0);" and @class="js-btns-enter btns-enter btns-enter-qq"]').click()
#切换到内置html进行登陆操作
drive.switch_to.frame("login_frame_qq")
drive.find_element_by_id('switcher_plogin').click()
#输入账户名密码
user_element = drive.find_element_by_xpath('//input[@id="u"]')
user_element.send_keys('414972363')
time.sleep(2)
password_element=drive.find_element_by_xpath('//input[@id="p"]')
password_element.send_keys('zjh19940413')

drive.find_element_by_xpath('//input[@id="login_button"]').click()

