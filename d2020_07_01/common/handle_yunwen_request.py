#-*- coding:utf-8 -*-
# @Time : 2020/8/5 15:26 
# @Author : wangj38
# @File : handle_yunwen_request.py 
# @Software: PyCharm
from d2020_07_01.common.myconfig import cnf
from d2020_07_01.common.mylog import logger
import requests
domain_url = cnf.read_section_to_dict("YUNWEN")['yun_wen_domaim_url']

class HandleYunWenRequest(object):
	def __init__(self,method,url,data):
		self.url=url
		self.method =method
		self.data =data

	def __handle_header(self):
		headers={"Content-Type" : "application/x-www-form-urlencoded"}
		return headers

	def __pre_url(self):
		if self.url.startswith("/"):
			return domain_url + self.url
		elif self.url.startswith('http://') or self.url.startswith("https://"):
			return self.url
		else:
			return domain_url + '/' + self.url
	def __handle_date(self):
		if self.data is not None and isinstance(self.data, str):
			if self.data.find('null') != -1:
				self.data = self.data.replace('null', "None")
			self.data = eval(self.data)
		return self.data
	def send_request(self):
		headers = self.__handle_header()
		data = self.__handle_date()
		url = self.__pre_url()
		if self.method.upper() == 'POST':
			try:
				res=requests.post(url=url,data=data,headers=headers)
			except Exception:
				e=logger.exception("发起post请求时候报错")
				raise e
			return res



