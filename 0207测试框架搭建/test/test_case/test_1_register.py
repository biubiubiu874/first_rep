# 对 requests 发送请求封装成类：
# #
# # 1， 支持 session 管理（可以定义 session 属性）
# # 2，封装 visit 方法（可以发送 get 和 post 请求）
from test.common.db_handler import DBHandler
from test.common.excel_handler import Excel
from test.common.helper import generate_mobile
from test.common.loggin_handler import LoggingHandler
from test.common.request_handler import HTTPrequests
import unittest

from test.common.yaml_handler import yaml_read
from test.libs import ddt
from test.config import config
# class HTTPrequests():
#     def __init__(self):
#         self.session = requests.Session()
#     def visit(self,method, url,headers,params=None, data=None, json=None,**kwargs):
#         res_get=self.session.request(method,url,headers=headers,params=params,data=data,json=json)
#         return res_get

# url = 'http://120.78.128.25:8766/futureloan/member/login'
# headers = {"X-Lemonban-Media-Type": "lemonban.v2"}
# data1 = {"mobile_phone": "18111111111", "pwd": "12345678"}
# data2 = {"mobile_phone": "18122", "pwd": "12"}
#
# requests=HTTPrequests()
# response=requests.visit('post',url,headers,json=data1)
# print(response)


excel = Excel(config.config.data_path,0)
text_data = excel.read_cell_values()
@ddt.ddt
class Test_1(unittest.TestCase):



    def setUp(self):
        self.requests2 = HTTPrequests()
        self.log_config=yaml_read(r'D:\PycharmProjects\test\config\yaml.yaml')
        self.loggin=LoggingHandler(self.log_config['logger']['name'],self.log_config['logger']['file'])

        self.db=DBHandler()

        # self.url = 'http://120.78.128.25:8766/futureloan/member/login'
        # self.headers = {"X-Lemonban-Media-Type": "lemonban.v2"}
        # self.data1 = {"mobile_phone": "18111111111", "pwd": "12345678"}
        # self.data2 = {"mobile_phone": "18122", "pwd": "12"}

    # def test_requests1(self):
    #     requests1=requesthandler.HTTPrequests()
    #     self.response1=requests1.visit(method='post',url=self.url,json=self.data1,headers=self.headers)
    #     expect1=200
    #     self.assertEqual(expect1,self.response1.status_code)
    #     requests1.session.close()
    def tearDown(self):
        self.requests2.session.close()
        self.db.close()


    @ddt.data(*text_data)
    def test_requests(self,text_data):
        #需要查询数据库
        #判断test_data['json']如果出现了#exist_phone#,使用generate_mobile随机生成一个手机号码，替换它。
        # if  '#exist_phone#' in text_data['json']:
        #     mobile=self.db.query('select * from member limit 1;')
        #
        #     text_data['json']=text_data['json'].replace('#exist_phone#',mobile)


        if '#new_phone#' in text_data['json']:
            while True:
                gen_mobile = generate_mobile()
                mobile=self.db.query('select * from member where mobile_phone=%s;',args=[gen_mobile])
                if not mobile:
                    text_data['json'] = text_data['json'].replace('#new_phone#', gen_mobile)
                    break







        try:
            self.response2=self.requests2.visit(method='post',url=str(config.config.host+text_data['url']),json=eval(text_data['json']),headers=eval(text_data['headers']))
            b=self.response2.json()
            expect=text_data['expected']

            self.assertEqual(expect,self.response2.json()['code'])



        except AssertionError as e:

            self.loggin.play_logger(e, 'ERROR')
            raise e