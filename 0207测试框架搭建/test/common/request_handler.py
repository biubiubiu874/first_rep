# 对 requests 发送请求封装成类：
# #
# # 1， 支持 session 管理（可以定义 session 属性）
# # 2，封装 visit 方法（可以发送 get 和 post 请求）

import requests
class HTTPrequests():
    def __init__(self):
        self.session = requests.Session()
    def visit(self,method, url,headers,params=None, data=None, json=None,**kwargs):
        res_get=self.session.request(method,url,headers=headers,params=params,data=data,json=json)
        return res_get

# url = 'http://120.78.128.25:8766/futureloan/member/login'
# headers = {"X-Lemonban-Media-Type": "lemonban.v2"}
# data1 = {"mobile_phone": "18111111111", "pwd": "12345678"}
# data2 = {"mobile_phone": "18122", "pwd": "12"}
#
# requests1=HTTPrequests()
# response=requests1.visit('post',url,headers,json=data1)
# print(response.json())
