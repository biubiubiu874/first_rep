"""
============================
Author:柠檬班-木森
Time:2020/3/5   11:03
E-mail:3247119728@qq.com
Company:湖南零檬信息技术有限公司
============================
"""
import unittest
import os
from library.ddt import ddt, data
from common.readexcel import ReadExcel
from common.handlepath import DATADIR
from common.handleconfig import conf
from common.handlerequests import SendRequest
from common.handlelog import log
from common.handle_data import replace_data

case_file = os.path.join(DATADIR, "apicases.xlsx")



@ddt
class TestLogin(unittest.TestCase):
    excel = ReadExcel(case_file, "login")
    cases = excel.read_data()
    request = SendRequest()


    @data(*cases)
    def test_login(self, case):
        # 第一步：准备用例数据
        url = conf.get("env", "url") + case["url"]
        method = case["method"]

        data = eval(replace_data(case["data"]))
        expected = eval(case["expected"])
        row = case["case_id"] + 1
        # 第二步：发送请求，获取结果
        response = self.request.send(url=url, method=method, json=data)
        res = response.json()
        # 第三步：断言（比对预期结果和实际结果）
        try:
            self.assert_dict_item(expected,res)

        except AssertionError as e:
            self.excel.write_data(row=row, column=8, value="未通过")
            log.error("用例：{}，执行未通过".format(case["title"]))
            log.exception(e)
            raise e
        else:
            self.excel.write_data(row=row, column=8, value="通过")
            log.info("用例：{}，执行通过".format(case["title"]))

    def assert_dict_item(self,dic1, dic2):
        """
        断言dic1中的所有元素都是diac2中的成员，成立返回True,不成立引发断言错误
        :param dic1: 字典
        :param dic2: 字典
        :return:
        """
        for item in dic1.items():
            if item not in dic2.items():
                raise AssertionError("{} items not in {}".format(dic1, dic2))


