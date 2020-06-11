# -*- coding:utf-8 -*-
# _author_='lijiachang'
# @time :2020/2/23 11:08

import os

class Config:
    # 项目路径
    root_path=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # 测试数据路径
    data_path=os.path.join(root_path,'data\cases.xlsx')

    # 测试用例路径
    cases_path=os.path.join(root_path,'test_case')

    # 测试报告路径
    report_path=os.path.join(root_path,'report')
    if not os.path.exists(report_path):
        os.mkdir(report_path)

class Devconfig(Config):
    # 项目的域名
    host = 'http://120.78.128.25:8766/futureloan'

config=Devconfig()
