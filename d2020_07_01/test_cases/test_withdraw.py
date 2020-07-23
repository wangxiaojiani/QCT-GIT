# -*- coding: utf-8 -*-
#@Time      :2020/7/15    19:24
#@Author    :xj
#@Email     :1027867874@qq.com
#@File      :test_withdraw.py
#@Software  :PyCharm
"""  提现类测试用例
http://www.lemfix.com/topics/393
"""
import unittest
from ddt import ddt,data
import re
import json
from d2020_07_01.common.mylog import logger
from d2020_07_01.common.handle_phone import get_old_phone
from d2020_07_01.common.handle_request import MyRequest
import jsonpath
from d2020_07_01.common.EnvData import EnvData
from d2020_07_01.common.myconfig import cnf
from d2020_07_01.common.read_excel import ReadExcel
from d2020_07_01.common.load_path import load_data_path
from d2020_07_01.common.EnvData import re_replace
from d2020_07_01.common.EnvData import clear_Envdata_attr
from d2020_07_01.common.handle_db import HandleDb
from decimal import *

sheet_name = cnf.read_section_to_dict("EXCEL")['withdraw']
datas =ReadExcel(load_data_path,sheet_name).load_data()
db = HandleDb()


@ddt
class TestWithDraw(unittest.TestCase):
    '提现类测试用例'

    @classmethod
    def setUpClass(cls):
        logger.info('========  start ============》开始执行{}类下的用例'.format(cls.__name__))
        clear_Envdata_attr()
        cls.count = 0
        user,pwd = get_old_phone()
        res =MyRequest('POST','/futureloan/member/login',{"mobile_phone":user,'pwd':pwd}).send_requests()
        cls.user_id = jsonpath.jsonpath(res.json(),'$..id')[0]
        cls.token = jsonpath.jsonpath(res.json(),'$..token')[0]
        setattr(EnvData,'user_id',cls.user_id)
        # 初始化余额
        db.update_data('UPDATE member SET leave_amount=9898.96 WHERE id={}'.format(cls.user_id))



    @classmethod
    def tearDownClass(cls):
        logger.info('========  END ============》{}类下的用例已经全部执行完成'.format(cls.__name__))
        db.db_close()

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
    def test_withdraw(self,case):
        '提现用例'

        if case['check_sql'] is not None and isinstance(case['check_sql'],str):
            if re.search("#(.*?)#",case['check_sql']):
                case['check_sql'] = re_replace(case['check_sql'],case['obj'])
                logger.info ('第{}条用例执行的sql语句是{}'.format (self.__class__.count, case['check_sql']))

                # 提现前的帐户余额
                pre_withdraw_amount =db.select_one_data(eval(case['check_sql'])['sql_01'])
                pre_withdraw_amount =str(Decimal(pre_withdraw_amount['leave_amount']).quantize(Decimal('0.00')))

                # 提现金额
                withdraw_amount = eval(case['param'])['amount']
                logger.info(withdraw_amount)

                if case['id'] ==5:
                    withdraw_amount=round(float(pre_withdraw_amount) + 1000.23,2)
                    setattr(EnvData,'max_amount',withdraw_amount)


                # 期望金额
                expect_amount = round((float(pre_withdraw_amount) * 100 - withdraw_amount *100)/100,2)
                setattr(EnvData,'expect_amount',expect_amount)

        if case['param'] is not None and isinstance (case['param'], str):
            if re.search ('#(.*?)#', case['param']):
                case['param'] = re_replace (case['param'], case['obj'])

        if case['expect_result'] is not None and isinstance(case['expect_result'],str):
            if re.search(r'#(.*?)#',case['expect_result']):
                case['expect_result'] = re_replace(case['expect_result'],case['obj'])

        expect_result = json.loads(case['expect_result'])
        res = MyRequest(case['method'],case['url'],case['param']).send_requests(self.__class__.token)


        try:
            self.assertEqual(expect_result['code'],res.json()['code'])
            self.assertEqual (expect_result['msg'], res.json ()['msg'])
            test_result=None
            if case['check_sql'] is not None and case['id'] !=5:
                logger.info ("第{}条用例期望结果{}".format (self.__class__.count,expect_result))
                # 获取结果返回结果
                final_amount = res.json()['data']['leave_amount']
                # 获取提现后数据库中查询的余额
                final_db_amount = db.select_one_data(eval(case['check_sql'])['sql_01'])
                final_db_amount = str (Decimal (final_db_amount['leave_amount']).quantize (Decimal ('0.00')))

                # 期望结果与接口返回结果比对
                self.assertEqual(expect_result['data']['leave_amount'],final_amount)

                # 期望结果与数据库中查询结果比对
                self.assertEqual (float(expect_result['data']['leave_amount']), float(final_db_amount))

                self.assertEqual(expect_result['data']['id'],res.json()['data']['id'])
            test_result = 'Pass'
        except AssertionError as e:
            logger.exception("第{}条用例执行-->【失败】".format(self.__class__.count))
            test_result = 'Failed'
            raise e
        finally:

            if res:
                self.t.write_back_data(self.__class__.count +1,8,str(res.json()))
                logger.info ("第{}条用例执行的实际结果{}回写成功".format (self.__class__.count, str (res.json ())))
                self.t.write_back_data(self.__class__.count+1,9,str(test_result))
                logger.info ("第{}条用例执行的测试结果{}回写成功".format (self.__class__.count, test_result))
            else:
                logger.info ("第{}条用例执行的实际结果与测试结果回写失败".format (self.__class__.count))














