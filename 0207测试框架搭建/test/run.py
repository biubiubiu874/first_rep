import  unittest
import  os
from test.common.HTMLTestRunnerNew import HTMLTestRunner
from test.config import config
import datetime

if __name__ == '__main__':
    # #初始化加载器
    testloder=unittest.TestLoader()
    # dir_name=os.path.dirname(os.path.abspath(__file__))
    # case_name=os.path.join(dir_name,'test_case')
    # #查找测试用例
    suite=testloder.discover(config.config.cases_path,"test_*.py")
    #添加测试报告
    # report_path=os.path.join(dir_name,'report')
    # if not os.path.exists(report_path):
    #     os.mkdir(report_path)
    file_path=os.path.join(config.config.report_path,'text_result_{}.html'.format(datetime.date.today()))
    with open(file_path,'wb') as f:
    #初始化运行器
        runner=HTMLTestRunner(f,
                              title="测试报告",
                              description="python自动化测试报告",
                              tester="lijiachang")
    #运行测试用例
        runner.run(suite)
