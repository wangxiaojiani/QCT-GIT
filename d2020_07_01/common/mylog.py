# -*- coding: utf-8 -*-
#@Time      :2020/6/17    21:13
#@Author    :xj
#@Email     :1027867874@qq.com
#@File      :mylog.py
#@Software  :PyCharm

import logging
import colorlog
from d2020_07_01.common.load_path import load_log_path
from d2020_07_01.common.myconfig import cnf
log_dict = cnf.read_section_to_dict('LOG') # 获取LOG下所有的option

class MyLog(logging.Logger):
    def __init__(self,name=log_dict["name"],level=log_dict["level"]):
        super().__init__(name,level)
        self.setLevel(level)
        self.fmt = logging.Formatter("%(asctime)s-%(name)s-【%(levelname)s】-%(filename)s-【%(lineno)d】:%(message)s")


    def my_log(self,file_path =None,ch_level=log_dict["ch_level"],fh_level=log_dict["fh_level"]):
        if not self.handlers:
            ch = logging.StreamHandler()
            ch.setLevel(ch_level)
            ch.setFormatter(self.fmt)
            self.addHandler (ch)
            if file_path:
                fh = logging.FileHandler(file_path,'a',encoding="utf-8")
                fh.setLevel(fh_level)
                fh.setFormatter(self.fmt)
                self.addHandler(fh)

logger = MyLog()
logger.my_log(load_log_path)


if __name__ == '__main__':

    logger = MyLog('root')
    logger.my_log("my_log.log")
    logger.info("kaka")
    s=None
    print(type(None))



