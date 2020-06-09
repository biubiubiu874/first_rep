"""
============================
Author:柠檬班-木森
Time:2020/3/17   20:37
E-mail:3247119728@qq.com
Company:湖南零檬信息技术有限公司
============================
"""
import unittest
import random
import jsonpath
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
class TestInterface(unittest.TestCase):
    excel = ReadExcel(case_file, "interface")
    cases = excel.read_data()
    request = SendRequest()
    db = DB()

    @classmethod
    def setUpClass(cls):
        """所有用例执行之前的环境准备：登录"""
        # 准备登录所需数据进行登录
        url = conf.get("env", "url") + "/user/login/"
        login_data = {
            "username": conf.get("test_data", "username"),
            "password": conf.get("test_data", "password")
        }
        response = cls.request.send(url=url, method="post", json=login_data)
        res = response.json()
        # 提取登录之后的token
        token = jsonpath.jsonpath(res, "$..token")[0]
        # 保存token
        CaseDate.token = "JWT" + " " + token

        # 准备添加项目的数据，添加一个项目
        pro_url = conf.get("env", "url") + "/projects/"
        pro_data = {
            "name": cls.random_project_name(),
            "leader": "lemonban",
            "tester": "木木木",
            "programmer": "zhang",
            "publish_app": "123",
            "desc": "jian"
        }
        headers = {
            "Authorization": getattr(CaseDate, "token")
        }
        # 发送请求添加项目
        response = cls.request.send(url=pro_url, method="post", json=pro_data, headers=headers)
        res2 = response.json()
        # 保存添加的项目id
        CaseDate.project_id= str(jsonpath.jsonpath(res2, "$..id")[0])
        # 保存添加的项目名
        CaseDate.pro_name = pro_data["name"]

    @data(*cases)
    def test_interface(self, case):
        # 第一步：准备用例数据
        url = conf.get("env", "url") + case["url"]
        method = case["method"]
        # 准备请求头
        headers = {
            "Authorization": getattr(CaseDate, "token")
        }
        # 替换用例数据中的参数化
        data = eval(replace_data(case["data"]))
        # 替换预期结果中的数据
        expected = eval(replace_data(case["expected"]))
        row = case["case_id"] + 1
        # 第二步：发送请求，获取结果
        response = self.request.send(url=url, method=method, json=data, headers=headers)
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

    @classmethod
    def random_project_name(cls):
        """随机生成一个项目名"""
        print("---name-")
        while True:
            s1 = random.choice(["前程贷", "开心贷", "新闻APP", "百度新闻", "秋秋"])
            number = random.randint(1, 999999)
            name = s1 + str(number)
            # 判断数据库中是否存在该用户名，
            res = cls.db.find_count("SELECT * FROM test.tb_projects WHERE name='{}'".format(name))
            if res == 0:
                return name
