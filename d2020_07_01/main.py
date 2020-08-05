# -*- coding: utf-8 -*-
#@Time      :2020/6/14    23:23
#@Author    :xj
#@Email     :1027867874@qq.com
#@File      :runner.py
#@Software  :PyCharm
import sys
sys.path.insert(0,'.')
import unittest
# from HTMLTestRunnerNew import HTMLTestRunner
import time
from d2020_07_01.common.load_path import load_test_path,load_test_report_path
from BeautifulReport import BeautifulReport
from d2020_07_01.test_cases.test_invest import TestInvest
from d2020_07_01.test_cases.test_chatlogbysession import TestChatBySession
from d2020_07_01.test_cases.test_recharge import TestRecharge
from d2020_07_01.test_cases.test_withdraw import TestWithDraw
from d2020_07_01.test_cases.test_loan import TestLoan
from d2020_07_01.common import EnvData


#第一种方法
# suit = unittest.TestSuite()
# loader = unittest.TestLoader()
# suit.addTests(loader.loadTestsFromTestCase(test_register.TestRegister))
# with open('report.html','wb') as f:
#     runner = HTMLTestRunner(stream=f,verbosity=2,description='测试注册',title='单元测试报告',tester='小贱')
#     runner.run(suit)



# 运行所有用例采用此方法
# loader = unittest.TestLoader()
# suit=loader.discover(load_test_path)

# 运行单独-》类测试用例 采用此方法
suit = unittest.TestSuite()
loader = unittest.TestLoader()
# # suit.addTest(loader.loadTestsFromTestCase(TestRecharge))
# suit.addTest(loader.loadTestsFromTestCase(TestWithDraw))
# suit.addTest(loader.loadTestsFromTestCase(TestInvest))
# suit.addTest(loader.loadTestsFromTestCase(TestLoan))
suit.addTest(loader.loadTestsFromTestCase(TestChatBySession))
# 生成表格式报告
# report= load_test_report_path + "/"+ time.strftime("%Y_%m_%d",time.localtime(time.time())).replace('/','_') + "_report.html"
# with open(report,'wb') as f:
#     runner = HTMLTestRunner(stream=f,verbosity=2,description='前程贷接口测试',title='单元测试报告',tester='小贱')
#     runner.run (suit)

# 生成图形式报告
runner=BeautifulReport(suit)
runner.report(description='测试报告',filename='report.html',report_dir=load_test_report_path)
