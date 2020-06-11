# 对 requests 发送请求封装成类：
# #
# # 1， 支持 session 管理（可以定义 session 属性）
# # 2，封装 visit 方法（可以发送 get 和 post 请求）
import json
from _pydecimal import Decimal

from jsonpath import jsonpath

from test.common.db_handler import DBHandler
from test.common.excel_handler import Excel
from test.common.loggin_handler import LoggingHandler
from test.common.request_handler import HTTPrequests
import unittest

from test.common.yaml_handler import yaml_read
from test.libs import ddt
from test.config import config
from test.middleware import loggin_info, context_data
from test.middleware.loggin_info import save_token

excel = Excel(config.config.data_path,2)
text_data = excel.read_cell_values()
@ddt.ddt
class Test_1(unittest.TestCase):
    def setUp(self):
        self.requests2 = HTTPrequests()
        self.log_config=yaml_read(r'D:\PycharmProjects\test\config\yaml.yaml')
        self.loggin=LoggingHandler(self.log_config['logger']['name'],self.log_config['logger']['file'])
        self.db = DBHandler()


        save_token()
        self.token=context_data.Context.token
        self.member_id=context_data.Context.member_id
        # self.before_money=context_data.Context.before_money

    def tearDown(self):
        self.requests2.session.close()
        self.db.close()


    @ddt.data(*text_data)
    def test_requests(self,text_data):
        try:
            # 获取充值前的账户余额
            querymoney = self.db.query('SELECT * from member where id=%s;', args=[self.member_id])
            before_money = jsonpath(querymoney, '$..leave_amount')[0]

            #替换测试用例里面的member_id
            if '#id#'in text_data['json']:

                text_data['json'] = text_data['json'].replace('#id#', str(self.member_id))
            elif 'wrong_member_id' in text_data['json']:
                text_data['json'] = text_data['json'].replace('#wrong_member_id#', str(self.member_id+1))

            # text_data['headers']={'X-Lemonban-Media-Type':'lemonban.v2 ','Authorization':self.token}
            headers=json.loads(text_data['headers'])
            headers['Authorization']=self.token

            # 发送充值请求
            self.response2=self.requests2.visit(method='post',
                                                url=str(config.config.host+text_data['url']),
                                                json=eval(text_data['json']),
                                                headers=headers)

            a=self.response2.json()

            #获取充值后的账户余额
            querymoney=self.db.query('SELECT * from member where id=%s;',args=[self.member_id])
            leave_money=jsonpath(querymoney,'$..leave_amount')[0]

            expect = text_data['expected']
            self.assertEqual(expect, self.response2.json()['code'])

            if a['code']==0:
                #计算预期的余额
                expect=before_money+eval((text_data['json']))['amount']
                #跟实际的做对比
                self.assertEqual(expect,leave_money)



        except AssertionError as e:

            self.loggin.play_logger(e, 'ERROR')
            raise e