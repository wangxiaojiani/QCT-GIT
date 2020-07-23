# -*- coding: utf-8 -*-
#@Time      :2020/7/19    23:57
#@Author    :xj
#@Email     :1027867874@qq.com
#@File      :test_invest.py
#@Software  :PyCharm
import unittest
from ddt import ddt,data
from d2020_07_01.common.myconfig import cnf
from d2020_07_01.common.mylog import logger
from d2020_07_01.common.EnvData import *
from d2020_07_01.common.read_excel import ReadExcel
from d2020_07_01.common.load_path import load_data_path
from d2020_07_01.common.handle_phone import *
from d2020_07_01.common.handle_request import MyRequest
import json
from  d2020_07_01.common.handle_db import HandleDb
from decimal import *


sheet_name = cnf.read_section_to_dict("EXCEL")['invest']
datas =ReadExcel(load_data_path,sheet_name).load_data()
db = HandleDb()

@ddt
class TestInvest(unittest.TestCase):
    '投资类用例'
    @classmethod
    def setUpClass(cls):
        logger.info ('========  start ============》开始执行{}类下的用例'.format (cls.__name__))
        clear_Envdata_attr()
        cls.count =0
    @classmethod
    def tearDownClass(cls):
        logger.info ('========  END ============》{}类下的用例已经全部执行完成'.format (cls.__name__))


    def setUp(self):
        logger.info (">" * 50)
        self.__class__.count += 1
        logger.info ("开始第>》》》   {}    《《《<条执行用例".format (self.__class__.count))
        self.t = ReadExcel(load_data_path,sheet_name)


    def tearDown(self):
        logger.info ("第>》》》   {}    《《《<条执行用例执行完成".format (self.__class__.count))
        logger.info ("<" * 50)
        self.t.close_excel()

    @data(*datas)
    def test_invest(self,case):
        person_symbol =None
        test_result = None
        expect_result =None


        if case['check_sql'] is not None and isinstance(case['check_sql'],str):
            if re.search('#(.*?)#', case['check_sql']):
                case['check_sql'] = re_replace(case['check_sql'])

                # 获取用户身份 是管理员还是普通用户以及id
                person_symbol=db.select_one_data(eval(case['check_sql'])['sql_01'])['type']
                max_count = db.select_one_data (eval (case['check_sql'])['sql_01'])['leave_amount']
                max_count= round(float(Decimal(max_count).quantize(Decimal('0.00'))))
                setattr(EnvData,"max_count",max_count)

                # 获取投资成功前financelog中用户的记录行数
                if len (eval (case['check_sql'])) >1: #
                    pre_line = db.get_count(eval(case['check_sql'])['sql_02'])

        if case['param'] is not None and isinstance(case['param'],str):
            if re.search('#(.*?)#',case['param']):
                if case['type'] =='before': # 前置条件设置为类属性
                    case['param'] = re_replace(case['param'])
                else:
                    case['param'] = re_replace(case['param'],case['obj']) # 用例作为单独用例设置为对象属性


        if case['type'] =='case':
            if case['expect_result'] is not None and isinstance (case['expect_result'], str):
                if re.search (r'#(.*?)#', case['expect_result']):
                    case['expect_result'] = re_replace (case['expect_result'], case['obj'])
            expect_result = json.loads(case['expect_result'])

        if hasattr(EnvData,'admin_member_token') and person_symbol ==0: # 管理员发起请求
            actual_result = MyRequest(case['method'],case['url'],case['param']).send_requests(EnvData.admin_member_token)
        elif hasattr(EnvData,'token') and person_symbol ==1:  # 普通角色发起请求
            actual_result = MyRequest(case['method'], case['url'], case['param']).send_requests(EnvData.token)
        else:
            actual_result =MyRequest(case['method'],case['url'],case['param']).send_requests()

        if case['extract_data']: # 响应结果中匹配出来的数据作为EnvData中的类属性，共所有用例使用
            extract_data_from_excel(case['extract_data'], actual_result.json())
            logger.info('==========EnvData环境类目前的类属性========={}'.format(EnvData.__dict__))
        if case['type'] == 'case':
            try:
                self.assertEqual(expect_result['code'],actual_result.json()['code'])
                self.assertEqual(expect_result['msg'],actual_result.json()['msg'])

                if  case['check_sql']  is not None:
                    if len (eval (case['check_sql'])) >1:
                        self.assertEqual (expect_result['data']['member_id'],
                                          actual_result.json ()['data']['member_id'])
                        self.assertEqual (expect_result['data']['loan_id'], actual_result.json ()['data']['loan_id'])
                        last_line = db.get_count(eval(case['check_sql'])['sql_02'])
                        self.assertEqual(pre_line+1,last_line)

                test_result = 'Passed'
            except AssertionError as e:
                logger.exception("第{}条用例执行-->【失败】".format(self.__class__.count))
                test_result = 'Failed'
                raise e
            finally:
                if actual_result:
                    self.t.write_back_data(self.__class__.count + 1, 10, str(actual_result.json()))
                    logger.info("第{}条用例执行的实际结果{}回写成功".format(self.__class__.count, str(actual_result.json())))
                    self.t.write_back_data(self.__class__.count + 1, 11, str(test_result))
                    logger.info("第{}条用例执行的测试结果{}回写成功".format(self.__class__.count, test_result))
                else:
                    logger.info("第{}条用例执行的实际结果与测试结果回写失败".format(self.__class__.count))











