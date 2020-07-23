# -*- coding: utf-8 -*-
#@Time      :2020/7/4    11:39
#@Author    :xj
#@Email     :1027867874@qq.com
#@File      :rp.py
#@Software  :PyCharm
import re
import json
import jsonpath
from d2020_07_01.common import handle_phone
from d2020_07_01.common.myconfig import cnf
from d2020_07_01.common.mylog import logger


class EnvData(object):
    old_phone = cnf.read_section_to_dict("PHONE")['mobile'] # 充值用例中用到
    def __init__(self):
        self.phone = handle_phone.check_phone() # 生成一个数据库中不存在的手机号码

def re_replace(target,obj=EnvData):
    """
    # 通过字符串正则匹配的方式将excel中读取参数化数据进行替换

     真实数据只从2个地方去获取：1个是配置文件当中的DATA区域 。另1个是，EvnData的类属性。

    :param target:字典中每个key对应的value
    :param obj: EnvData类的实例对象
    :return:
    """
    p = "#(.*?)#"
    while re.search(p,target):
        ret=re.search(p,target)
        key = ret.group(1)
        try:
            value= cnf.read_section_to_dict('DATA')[key]
        except:
            try:
                value = getattr(obj,key)
            except Exception:
                logger.info("EnvData类中不存在此【{}】".format(key))
                raise

        target = re.sub(p,str(value),target,count=1)
    return target


# 通过字符串find的方式将excel中读取参数化数据进行替换
def replace_mark_with_data(case,mark,real_data):
    for key,value in case.items():
        if value is not None and isinstance(value,str):
            if value.find(mark) != -1:
                case[key] = value.replace(mark,real_data)
    return case

def clear_Envdata_attr():
    """
    清除EnvData类中的类属性
    :return:
    """

    values = EnvData.__dict__ # 得到的<class 'mappingproxy'>
    for key,value in dict(values).items():
        if key.startswith('__') or key == 'old_phone':
            pass
        else:
            delattr(EnvData,key)
            print(EnvData.__dict__)

def extract_data_from_excel(extract_exprs,response_dict):
  """
    该方法本项目主要应用在业务流上
    根据jsonpath提取表示式，从响应结果中匹配出来的数据作为EnvData中的类属性，共所有用例使用
  :param extract_exprs:excel中读取出来的提取表达式字符串
  :param response_dict:请求之后的响应结果
  :return:
  """
  extract_dict =json.loads(extract_exprs) # 将从excel中读取出的提取表达式转换为字典
  for key,value in extract_dict.items():
      res = str(jsonpath.jsonpath(response_dict,value)[0]) #匹配到数据返回列表 匹配不到返回false
      if res :
          setattr(EnvData,key,res)



if __name__ == '__main__':
    print(EnvData.__dict__ )







