#-*- coding:utf-8 -*-
# @Time : 2020/8/5 15:49 
# @Author : wangj38
# @File : test_chatlogbysession.py 
# @Software: PyCharm
from ddt import ddt,data
from d2020_07_01.common.mylog import logger
from d2020_07_01.common.load_path import load_yunwen_data_path
from d2020_07_01.common.read_excel import ReadExcel
from d2020_07_01.common.myconfig import cnf
from d2020_07_01.common.EnvData import re_replace
import unittest
from  jsonpath import jsonpath
import json
from d2020_07_01.common.handle_yunwen_request import HandleYunWenRequest
import re
sheet_name = cnf.read_section_to_dict("EXCEL")['chatbysession']
datas = ReadExcel(load_yunwen_data_path,sheet_name).load_data()



@ddt
class TestChatBySession(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		logger.info('开始执行获取访客会话用例')
		cls.count =0
	@classmethod
	def tearDownClass(cls) -> None:
		logger.info('结束执行获取会话用例')

	def setUp(self) -> None:
		self.__class__.count +=1
		logger.info('当前执行第{}条测试用例'.format(self.__class__.count))
	def tearDown(self) -> None:
		logger.info('第{}条测试用例执行结束'.format(self.__class__.count))

	@data(*datas)
	def test_chart_by_session(self,case):
		if case['param'] is not None and isinstance(case['param'],str):
			if re.search(r'#(.*?)#',case['param']):
				case['param'] = re_replace(case['param'])
		expect_result = json.loads(case['expect_result'])
		res = HandleYunWenRequest(case['method'],case['url'],case['param']).send_request()

		try:
			self.assertEqual(res.json()['code'],expect_result['code'])
			self.assertEqual(res.json()['codeDesc'],expect_result['codeDesc'])
		except AssertionError as e:
			logger.exception("第{}条用例执行-->【失败】".format(self.__class__.count))
			raise e
		else:
			logger.info(("第{}条用例执行-->【成功】".format(self.__class__.count)))

