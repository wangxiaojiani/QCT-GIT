# -*- coding: utf-8 -*-
#@Time      :2020/6/14    22:29
#@Author    :xj
#@Email     :1027867874@qq.com
#@File      :test_register.py
#@Software  :PyCharm

import unittest
from ddt import ddt,data
import json
import re
from d2020_07_01.common.handle_request import MyRequest
from d2020_07_01.common.read_excel import ReadExcel
from d2020_07_01.common.mylog import logger
from d2020_07_01.common.load_path import load_data_path
from d2020_07_01.common.myconfig import cnf
from d2020_07_01.common.handle_db import HandleDb
from d2020_07_01.common.EnvData import re_replace


sheet_name = cnf.read_section_to_dict("EXCEL")["register"] # 读取配置文件中register表数据
datas = ReadExcel (load_data_path,sheet_name).load_data ()
db = HandleDb()

@ddt
class TestRegister(unittest.TestCase):
    "注册类用例"

    @classmethod
    def setUpClass(cls):
        logger.info('========  start ============》开始执行{}类下的用例'.format(cls.__name__))
        cls.count = 0

    @classmethod
    def tearDownClass(cls):
        logger.info('========  END ============》{}类下的用例已经全部执行完成'.format(cls.__name__))

    def setUp(self):
        logger.info(">" * 50)
        self.__class__.count += 1
        logger.info("开始第>》》》   {}    《《《<条执行用例".format(self.__class__.count))
        self.t = ReadExcel (load_data_path, sheet_name)

    def tearDown(self):
        logger.info ("第>》》》   {}    《《《<条执行用例执行完成".format(self.__class__.count))
        logger.info ("<" * 50)
        self.t.close_excel()

    @data(*datas)
    def test_register(self,case):
        '注册用咧'
        # 对excel中已经参数化的内容进行替换
        if case["param"] is not None and isinstance (case["param"], str):
            if re.search (r'#(.*?)#', case['param']):
                case['param'] = re_replace (case['param'], case["obj"])
        if case["check_sql"] is not None and isinstance (case["check_sql"], str):
            if re.search (r'#(.*?)#', case["check_sql"]):
                case['check_sql'] = re_replace (case['check_sql'], case["obj"])

        expect_result = json.loads(case["expect_result"])
        actual_result = MyRequest(case['method'], case['url'],case['param']).send_requests()
        # test_result=None
        try:
            logger.info("第{}条用例期望结果{}".format(self.__class__.count,expect_result))
            self.assertEqual(actual_result.json()["code"],expect_result["code"])
            self.assertEqual(actual_result.json()["msg"],expect_result["msg"])
            if case['check_sql']: # 如果excel中check_sql字段有sql则进行校验
                logger.info('第{}条用例执行的sql语句是{}'.format(self.__class__.count,case['check_sql']))
                result = db.select_one_data(case['check_sql'])
                self.assertIsNotNone(result)
            # self.assertEqual(actual_result,case["expect_result"])
            logger.info("第{}条用例执行-->【通过】".format(self.__class__.count))
            test_result = "Pass"
        except AssertionError as e:
            logger.exception("第{}条用例执行-->【失败】".format(self.__class__.count))
            test_result = "Fail"
            raise e
        finally: # 数据 回写
             if actual_result is not None:
                 self.t.write_back_data(self.__class__.count +1,8,str(actual_result.json()))
                 logger.info ("第{}条用例执行的实际结果{}回写成功".format (self.__class__.count,str(actual_result.json())))
                 self.t.write_back_data(self.__class__.count +1,9,test_result)
                 logger.info ("第{}条用例执行的测试结果{}回写成功".format (self.__class__.count, test_result))
             else:
                 logger.info ("第{}条用例执行的实际结果与测试结果回写失败".format(self.__class__.count))

