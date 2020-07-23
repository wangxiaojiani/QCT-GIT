#-*- coding:utf-8 -*-
# @Time : 2020/7/22 10:46 
# @Author : wangj38
# @File : test_loan.py 
# @Software: PyCharm
"""加标/新增项目接口"""
import re
import jsonpath
import json
import unittest
from d2020_07_01.common.mylog import logger
from d2020_07_01.common.EnvData import clear_Envdata_attr
from d2020_07_01.common.EnvData import EnvData
from ddt import ddt,data
from d2020_07_01.common.myconfig import cnf
from d2020_07_01.common.read_excel import ReadExcel
from d2020_07_01.common.load_path import load_data_path
from d2020_07_01.common.EnvData import re_replace
from  d2020_07_01.common.handle_request import MyRequest
from d2020_07_01.common.EnvData import extract_data_from_excel
from d2020_07_01.common.handle_db import HandleDb


sheet_name = cnf.read_section_to_dict("EXCEL")['loan']
datas = ReadExcel(load_data_path,sheet_name).load_data()
db = HandleDb()

@ddt
class TestLoan(unittest.TestCase):
    '加标类测试'

    @classmethod
    def setUpClass(cls):
        logger.info("------------>开始执行{} 类下的测试用例集     <-----------------".format(cls.__name__))
        cls.count = 0
        clear_Envdata_attr() # 清理环境类中的类属性

    @classmethod
    def tearDownClass(cls):
        logger.info("------------>结束执行{} 类下的测试用例集     <-----------------".format(cls.__name__))

    def setUp(self):
        self.__class__.count +=1
        logger.info("---------->开始执行第{}条测试用例-----------------".format(self.__class__.count))
        self.t = ReadExcel(load_data_path,sheet_name)

    def tearDown(self):
        self.t.close_excel()
        logger.info("---------->结束执行第{}条测试用例-----------------".format(self.__class__.count))

    @data(*datas)
    def test_loan(self,case):
        test_result =None
        # 前置sql

        if case['check_sql'] is not None and isinstance(case['check_sql'],str):
            if re.search(r"(.*?)",case['check_sql']):
                case['check_sql'] = re_replace(case['check_sql'])
                logger.info('打印出sql-=============》{}'.format(eval(case['check_sql'])['sql_01']))
                loan_id= db.select_one_data(eval(case['check_sql'])['sql_01'])['id']
                logger.info("{}".format(loan_id))

                expect_line= db.get_count(eval(case['check_sql'])['sql_02'])

                setattr(EnvData,"loan_id",loan_id)


        if case['param'] is not None and isinstance(case['param'],str):
            if re.search(r"(.*?)",case["param"]):
                case["param"] = re_replace(case['param'])

        if case['expect_result'] is not None and isinstance(case['expect_result'],str):
            if re.search(r"(.*?)",case['expect_result']):
                case["expect_result"] =re_replace(case["expect_result"])
            expect_result = json.loads(case["expect_result"])
            logger.info("*****************用列的期望结果为{}".format(expect_result))
        if hasattr(EnvData,"admin_member_token"):
            actual_result = MyRequest(case['method'],case['url'],case['param']).send_requests(EnvData.admin_member_token)
        else:
            actual_result = MyRequest(case['method'],case['url'],case['param']).send_requests()

        if case['extract_data']:
            extract_data_from_excel(case['extract_data'],actual_result.json())
        try:
            if case['type'] == 'case':
                self.assertEqual(expect_result['code'],actual_result.json()['code'])
                self.assertEqual(expect_result['msg'],actual_result.json()['msg'])
                if case['check_sql']:
                    self.assertFalse(expect_result['data']['id']>=actual_result.json()['data']['id'])
                    last_line  = db.get_count(eval(case['check_sql'])['sql_02'])
                    logger.info("expect_line----------->{}".format(expect_line))
                    logger.info("last_line----------->{}".format(last_line))
                    self.assertFalse(expect_line >= last_line)
                test_result = "PASS"
        except AssertionError as e :
            logger.exception("---------->第{}条测试用例断言错误----------------".format(self.__class__.count))
            test_result = "Failed"
            raise e
        finally:
            if actual_result:
                self.t.write_back_data(self.__class__.count+1,10,str(actual_result.json()))
                self.t.write_back_data(self.__class__.count+1,11,str(test_result))
            logger.info("---------->第{}条测试用列回写失败---------".format(self.__class__.count))










