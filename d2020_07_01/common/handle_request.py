#-*- coding:utf-8 -*-
# @Time : 2020/6/30 17:42 
# @Author : wangj38
# @File : handle_request.py 
# @Software: PyCharm
import requests
from d2020_07_01.common.myconfig import cnf
from d2020_07_01.common.mylog import logger
from d2020_07_01.common.handle_rsa import generator_sign
import json
domain_url =cnf.read_section_to_dict("DOMAIN")["ip"]

class MyRequest(object):
    def __init__(self,method,url,data):
        self.url =url
        self.method =method
        self.data =data

    def __handle_header(self,token=None,**kwargs):
        """
        处理请求头，根据项目情况设置必要的请求头部参数
        :param token:传递的token数值
        :param kwargs:动态设置请求头信息
        :return:请求头
        """
        headers = {"Content-Type" : "application/json",
                   # 为了兼容v3版本 所以将v3版本的auth_type 设置到了配置文件中
                "X-Lemonban-Media-Type" : cnf.read_section_to_dict("DOMAIN")["auth_type"]}

        if token:
            headers["Authorization"] ="Bearer {}".format(token)
        for key,value in kwargs.items():
            if key not in headers.keys():
                headers[key] =value
        return headers

    def __pre_url(self):
        """
        对excel中url是否带'/'进行兼容处理
        :return:
        """

        if self.url.startswith('/'):
            return domain_url + self.url
        elif self.url.startswith('http://') or self.url.startswith("https://"):  # 加上这个判断视为了考虑到mock服务
            return self.url
        else:
            return domain_url + '/' + self.url

    def __pre_data(self,token=None):
        """
        对excel中所传的字典参数进行处理
        :return:
        """
        if self.data is not None and isinstance (self.data, str):
            # param = json.loads (self.data)
            if self.data.find('null') != -1:
                self.data = self.data.replace('null',"None")
            param = eval(self.data)   # 这里用eval 可以自动计算excel总编辑的表达式

        # 如果是v3版本需要I加上签名
        if cnf.read_section_to_dict("DOMAIN")['auth_type'] == "lemonban.v3" and token is not None:
            sign,time_stamp = generator_sign(token)
            param["sign"] = sign
            param["timestamp"] = time_stamp
            return param
        return self.data

    def send_requests(self,token=None,cookie=None,**kwargs):
        # 获取请求头部信息
        headers = self.__handle_header(token,**kwargs)

        # 对excel中url是否带'/'进行兼容处理
        url = self.__pre_url ()

        # 对excel中接口所传的字符串类型的字典参数进行json化处理
        data=self.__pre_data (token)

        logger.info ("请求头 -> {}".format (headers))
        logger.info ("请求方法 -> {}".format (self.method))
        logger.info ("请求体 -> {}".format (data))
        # 根据方法进行调用
        if self.method.upper() == "POST":
            try:
                res = requests.post(url,json=data,headers=headers,cookies=cookie)
            except Exception:
                e = logger.exception("调用post封装方法，请求{}地址时出错".format(url))
                raise e
        elif self.method.upper() =='PATCH':
            try:
                logger.info("======>>>开始执行patch请求，数据为{} 类型为{}".format(data,type(data)))
                logger.info("======>>>开始执行patch请求，请求投为为{} 类型为{}".format(headers,type(headers)))

                res = requests.patch(url,json=data,headers=headers,cookies=cookie)
            except Exception:
                e=logger.exception("调用patch封装方法，请求{}地址时出错".format(url))
                raise e
        else:
            try:
                res =requests.get(url,params=data,headers=headers,cookies=cookie)

            except Exception:
                e = logger.exception ("调用post封装方法，请求{}地址时出错".format (url))
                raise e
        logger.info ("响应状态码 -> {}".format (res.status_code))
        logger.info("响应头 -> {}".format(res.headers))
        logger.info ("响应体【实际结果】 -> {}".format (res.json()))
        return res
if __name__ == '__main__':

    login_url = "/futureloan/member/login"
    login_datas = {"mobile_phone": "13296662570", "pwd": "12345678"}
    resp = MyRequest("post",login_url,login_datas).send_requests()
    print(resp.text)
    token = resp.json()['data']['token_info']['token']
    memberid = resp.json()['data']['id']
    # recharge_url ="http://api.lemonban.com/futureloan/member/recharge"
    # recharge_data='{"member_id": memberid, "amount": 2000}'
    # resp=MyRequest("post",recharge_url,recharge_data).send_requests(token)
    # print(resp.json())
    add_url = "/futureloan/loan/add"
    add_datas = {
    "member_id":memberid,
    "title":"借款项目01",
    "amount":500000.00,
    "loan_rate":18.0,
    "loan_term":6,
    "loan_date_type":1,
    "bidding_days":10}
    resp = MyRequest("post", add_url, add_datas).send_requests(token)
    print(resp.text)
    loan_id = resp.json()['data']['id']
    loan_url="/futureloan/loan/audit"
    loan_data={"approved_or_not":'true',"loan_id": loan_id}
    resp22=MyRequest('patch',loan_url,loan_data).send_requests(token)
    print(resp22.json())





