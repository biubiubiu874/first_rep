"""
============================
Author:柠檬班-木森
Time:2020/2/21   20:37
E-mail:3247119728@qq.com
Company:湖南零檬信息技术有限公司
============================
"""
import unittest
import random
import os
from library.ddt import ddt, data
from common.readexcel import ReadExcel
from common.handlepath import DATADIR
from common.handleconfig import conf
from common.handlerequests import SendRequest
from common.handlelog import log
from common.connectdb import DB
from common.handle_data import replace_data, CaseDate

case_file = os.path.join(DATADIR, "apicases.xlsx")


@ddt
class TestRegister(unittest.TestCase):
    excel = ReadExcel(case_file, "register")
    cases = excel.read_data()
    request = SendRequest()
    db = DB()

    def setUp(self):
        """测试用例运行前运行"""
        # 随机生成一个用户名，保存
        CaseDate.name = self.random_name()

    @data(*cases)
    def test_register(self, case):
        # 第一步：准备用例数据
        url = conf.get("env", "url") + case["url"]
        method = case["method"]
        # 替换用例数据
        data = eval(replace_data(case["data"]))
        # 替换预期结果中的数据
        expected = eval(replace_data(case["expected"]))
        row = case["case_id"] + 1
        # 第二步：发送请求，获取结果
        response = self.request.send(url=url, method=method, json=data)
        res = response.json()
        try:
            self.assert_dict_item(expected, res)
        except AssertionError as e:
            self.excel.write_data(row=row, column=8, value="未通过")
            log.error("用例：{}，执行未通过".format(case["title"]))
            log.exception(e)
            raise e
        else:
            self.excel.write_data(row=row, column=8, value="通过")
            log.info("用例：{}，执行通过".format(case["title"]))

    def assert_dict_item(self, dic1, dic2):
        """
        断言dic1中的所有元素都是diac2中的成员，成立返回True,不成立引发断言错误
        :param dic1: 字典
        :param dic2: 字典
        :return:
        """
        for item in dic1.items():
            if item not in dic2.items():
                raise AssertionError("{} items not in {}".format(dic1, dic2))

    def random_name(self):
        """随机生成一个用户名"""
        print("---name-")
        while True:
            s1 = random.choice(["a", "b", "c", "d", "e"])
            number = random.randint(1, 999999)
            name = s1 + str(number)
            # 判断数据库中是否存在该用户名，
            res = self.db.find_count("SELECT * FROM test.auth_user WHERE username='{}'".format(name))
            if res == 0:
                return name
