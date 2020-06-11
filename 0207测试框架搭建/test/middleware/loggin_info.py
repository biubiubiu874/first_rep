# -*- coding:utf-8 -*-
# _author_='lijiachang'
# @time :2020/2/26 22:41
from _pydecimal import Decimal

from test.common.request_handler import HTTPrequests
from jsonpath import  jsonpath
from test.middleware import context_data

def login():
    """登陆，返回token和member_id"""
    #测试账号    user：18813758109   密码：12345678
    request_login=HTTPrequests()
    res=request_login.visit(method='post',
                            url='http://120.78.128.25:8766/futureloan/member/login',
                            json={'mobile_phone': '18813758109','pwd': '12345678'},
                            headers={'X-Lemonban-Media-Type':'lemonban.v2 '})
    return res

def save_token():
    data = login().json()
    # print(data)
    member_id = jsonpath(data, '$..id')[0]
    token = jsonpath(data, '$..token')[0]
    token_type = jsonpath(data, '$..token_type')[0]
    # leave_amount=Decimal(jsonpath(data,'$..leave_amount')[0])
    # print(leave_amount)
    token_haha = ' '.join([token_type,token])

    context_data.Context.token=token_haha
    context_data.Context.member_id=member_id
    # context_data.Context.before_money=leave_amount



    return  {'token':token,'member_id':member_id}


if __name__ == '__main__':
    print(save_token())