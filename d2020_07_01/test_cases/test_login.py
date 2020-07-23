# -*- coding: utf-8 -*-
#@Time      :2020/7/7    21:23
#@Author    :xj
#@Email     :1027867874@qq.com
#@File      :test_login.py
#@Software  :PyCharm
import unittest
from d2020_07_01.common.mylog import logger
from d2020_07_01.common.myconfig import cnf
from d2020_07_01.common.read_excel import ReadExcel
from d2020_07_01.common.load_path import load_data_path
from ddt import ddt,data
from d2020_07_01.common.EnvData import re_replace
import re
import json
from d2020_07_01.common.handle_request import MyRequest


sheet_name = cnf.read_section_to_dict("EXCEL")["login"] # 读取配置文件中login表数据
datas = ReadExcel(load_data_path,sheet_name).load_data()

@ddt
class TestLogin(unittest.TestCase):
    "登录类测试用例"

    @classmethod
    def setUpClass(cls):
        logger.info('========  start ============》开始执行{}类下的用例'.format(cls.__name__))
        cls.count = 0

    @classmethod
    def tearDownClass(cls):
        logger.info ('========  END ============》{}类下的用例已经全部执行完成'.format (cls.__name__))

    def setUp(self):
        logger.info(">" * 50)
        self.__class__.count +=1
        logger.info ("开始第>》》》   {}    《《《<条执行用例".format (self.__class__.count))
        self.t = ReadExcel (load_data_path, sheet_name)

    def tearDown(self):
        logger.info ("第>》》》   {}    《《《<条执行用例执行完成".format (self.__class__.count))
        logger.info ("<" * 50)
        self.t.close_excel ()

    @data(*datas)
    def test_login(self,case):
        '登录用例'
        if case["param"] is not None and isinstance(case['param'],str):
            if re.search(r"#(.*?)#",case['param']):
                case['param']=re_replace(case['param'],case['obj'])

        expect_result = json.loads(case['expect_result'])
        actual_result = MyRequest(case['method'],case['url'],case['param']).send_requests()

        try:
            logger.info ("第{}条用例期望结果{}".format (self.__class__.count, expect_result))
            self.assertEqual(actual_result.json()['code'],expect_result['code'])
            self.assertEqual(actual_result.json()['msg'],expect_result['msg'])
            test_result = 'Pass'
            logger.info ("第{}条用例执行-->【通过】".format (self.__class__.count))
        except AssertionError as e:
            logger.exception ("第{}条用例执行-->【失败】".format (self.__class__.count))
            test_result ='Failed'
            raise e
        finally:
            if actual_result is not None:
                self.t.write_back_data(self.__class__.count + 1,8,str(actual_result.json()))
                logger.info ("第{}条用例执行的实际结果{}回写成功".format (self.__class__.count, str (actual_result.json ())))
                self.t.write_back_data(self.__class__.count +1,9,test_result)
                logger.info ("第{}条用例执行的测试结果{}回写成功".format (self.__class__.count, test_result))
            else:
                logger.info ("第{}条用例执行的实际结果与测试结果回写失败".format (self.__class__.count))



