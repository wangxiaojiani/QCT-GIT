# -*- coding: utf-8 -*-
#@Time      :2020/7/7    22:28
#@Author    :xj
#@Email     :1027867874@qq.com
#@File      :test_recharge.py
#@Software  :PyCharm

import unittest
from ddt import ddt,data
import json
import re
from decimal import *
from d2020_07_01.common.handle_request import MyRequest
from d2020_07_01.common.read_excel import ReadExcel
from d2020_07_01.common.mylog import logger
from d2020_07_01.common.load_path import load_data_path
from d2020_07_01.common.myconfig import cnf
from d2020_07_01.common.handle_db import HandleDb
from d2020_07_01.common.EnvData import re_replace,EnvData,clear_Envdata_attr
from d2020_07_01.common.handle_phone import get_old_phone
import jsonpath


sheet_name = cnf.read_section_to_dict("EXCEL")["recharge"] # 读取配置文件中recharge表数据
datas = ReadExcel (load_data_path,sheet_name).load_data ()
db = HandleDb()

@ddt
class TestRecharge(unittest.TestCase):
    "充值类用例"

    @classmethod
    def setUpClass(cls):
        logger.info('========  start ============》开始执行{}类下的用例'.format(cls.__name__))
        clear_Envdata_attr() # 清除上个脚本设置的动态属性
        cls.count = 0
        user,pwd = get_old_phone()
        res = MyRequest('POST','/futureloan/member/login',{"mobile_phone":user,"pwd":pwd}).send_requests()
        cls.user_id = jsonpath.jsonpath(res.json(),'$..id')[0]
        setattr(EnvData,'user_id',cls.user_id)
        cls.token = jsonpath.jsonpath(res.json(),'$..token')[0]

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
    def test_recharge(self,case):
        '充值用咧'
        # 对excel中已经参数化的内容进行替换
        if case["param"] is not None and isinstance (case["param"], str):
            if re.search (r'#(.*?)#', case['param']):
                case['param'] = re_replace (case['param'], case["obj"])
        if case["check_sql"] is not None and isinstance (case["check_sql"], str):
            if re.search (r'#(.*?)#', case["check_sql"]):
                case['check_sql'] = re_replace (case['check_sql'], case["obj"])

            logger.info ('第{}条用例执行的sql语句是{}'.format (self.__class__.count, case['check_sql']))
            # 充值前的金额
            pre_result = db.select_one_data (eval(case['check_sql'])["sql_01"])
            pre_amount = pre_result['leave_amount'] # 因为从数据库获取的是小数 数据库传过来的字符类型为DECIMAL  类所以要进行转化；也可以通过数据库查询cast方法在sql内部转化为字符串
            pre_amount = str(pre_amount.quantize(Decimal('0.00'))) #'0.00'保留两位小数并转换为字符串

            # 验证是否在log表中增加一条记录所以需要获取充值之前与充值之后的行数
            pre_line = db.select_one_data(eval(case['check_sql'])["sql_02"])


            # 充值金额
            add_mount = eval (case['param'])['amount']
            case['leave_amount'] = round((float(pre_amount)*100 + add_mount * 100)/100,2)
            setattr(EnvData,'leave_amount',case['leave_amount'])

        if case["expect_result"] is not None and isinstance (case["expect_result"], str):
            if re.search (r'#(.*?)#', case["expect_result"]):
                case['expect_result'] = re_replace (case['expect_result'], case["obj"])


        expect_result = json.loads(case["expect_result"])
        actual_result = MyRequest(case['method'], case['url'],case['param']).send_requests(self.__class__.token)
        # test_result=None
        try:
            logger.info("第{}条用例期望结果{}".format(self.__class__.count,expect_result))
            self.assertEqual(actual_result.json()["code"],expect_result["code"])
            self.assertEqual(actual_result.json()["msg"],expect_result["msg"])
            #这里还要进行金额校验

            if case['check_sql']: # 如果excel中check_sql字段有sql则进行校验
                # 充值后金额
                final_result = db.select_one_data(eval(case['check_sql'])["sql_01"])
                final_amount = final_result['leave_amount']
                final_amount = str(final_amount.quantize(Decimal('0.00')))

                # 获取充值后log表中返回的行数
                final_line = db.select_one_data(eval(case['check_sql'])["sql_02"])


                # 预期结果与数据库查询结果leave_amount进行比对
                self.assertEqual(case['leave_amount'] ,float(final_amount))

                # 预期结果与接口返回leave_amount进行比对
                self.assertEqual(case['leave_amount'],actual_result.json()["data"]['leave_amount'])

                # 数据库中是否增加日志进行比对
                self.assertEqual(pre_line['count']+1,final_line['count'])

                # 预期结果与接口返回用户id进行比对
                self.assertEqual(final_result['id'],self.__class__.user_id)
                # self.assertIsNotNone(result)
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

