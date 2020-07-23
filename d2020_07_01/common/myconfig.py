# -*- coding: utf-8 -*-
#@Time      :2020/6/19    22:32
#@Author    :xj
#@Email     :1027867874@qq.com
#@File      :myconfig.py
#@Software  :PyCharm
"""
1. 配置文件中用get读取出来的数据都是字符串 通常在配置文件中字符串是不用加引号的，但这里封装时考虑到统一处理数据类型，故如果value是字符串，也要加上引号
2.value值写入配置文件时也要进行相应的数据类型进行处理 否则读取时会报错
"""

import os
from configparser import ConfigParser
from d2020_07_01.common.load_path import load_ini_path

class MyConfig(ConfigParser):
    def __init__(self):
        super().__init__()
        self.path = load_ini_path
        if not os.path.isfile(self.path):
            e =Exception("配置文件【{}】路径错误，请认真核对".format(self.path))
            raise e
        self.read(self.path,encoding="utf-8")

    def check_section(self,section):
        '检验配置文件中是否有对应的section'
        try:
            self.items(section) # 输出该section中对应的列表[(key1,value1),(key2,value2)]
        except Exception:
            print("配置文件{}中没有对应的section->{}".format(self.path,section))
            return
        return True

    def read_sections(self):
        '读取配置文件，并获取所有的section 返回值为列表'
        return self.sections()

    def read_one_section(self,section):
        "读取一个section list里面是元祖"
        if not self.check_section(section):
            return
        return self.items(section) # 这里需要注意一下option读取出来全部都是小写的  所以最好配置文件中option就是小写 避免出错

    def read_section_to_dict(self,section):
        '读取一个section到字典中'
        res = dict()
        for key,value in self.read_one_section(section):
            res[key] = eval(value) # 【统一处理数据类型】
        return res # 返回字典

    def read_all_section_to_dict(self):
        '读取所有的section到字典中'
        sections_list = self.sections()
        final_res = dict()
        for section in sections_list:
            final_res[section] = self.read_section_to_dict(section)
        return final_res    # section 为key

    def remove_one_option(self,section,option):
        '删除section中的一项option'
        if not self.check_section(section):
            return
        return self.remove_option(section,option)

    def remove_one_section(self,section):
        '删除整个section'
        if not self.check_section(section):
            return
        return self.remove_section(section) # 返回的是boolean

    def add_one_section(self,section):

        if section in self.sections():
            return
        self.add_section (section)

    def add_one_option(self,section,option,value):
        '在section中添加或者修改option与value VALUE为字符串 及时是None也要写成"None"'
        if not self.check_section(section):
            return
        if option in self.options(section):
            print ("option-->【{}】在section-->【{}】中已经存在，故进行修改".format (option, section))
        else:
            print ("option-->【{}】在section-->【{}】中不存在，故进行添加".format (option, section))
        try:
            tt = type(eval(value))
            if tt in [list,dict,tuple,int,float,bool,set] or value.upper() =='NONE':
                self.set (section, option, '{}'.format (value))
        except Exception:
            self.set (section, option, '\"{}\"'.format (value))


    def do_action(self):
        "执行write写入, remove和set方法并没有真正的修改ini文件内容，只有当执行write()方法的时候 才会执行"
        self.write(open(self.path,"w",encoding="utf-8"))


cnf = MyConfig()


if __name__ == '__main__':


    # print(cnf.items("USER"))
    # print(cnf.sections())
    # print(cnf.options("USER"))
    # cnf.set("mm","cb","11d2222Ad1a1") #键会自动转为小写，建存在覆盖 建不存在新建

    # cnf.add_section("sess")
    # cnf.set("sess","dd","dad")
    # cnf.write(open(load_ini_path,"w",encoding="utf-8"))
    s=MyConfig()
    # s.check_section("mm")
    # s=cnf.r_option("USER",'A')
    # print(s)
    # print(type(s))
    # # cnf.get
    #
    # s.add_one_option("USER","KK1","(1,2,3)")
    # s.add_one_option ("USER", "KK2", "[1,2,3]")
    # s.add_one_option ("USER", "KK3", '{"name":1,"age":2}')
    # s.add_one_option ("USER", "KK4", "False")
    # s.add_one_option ("USER", "KK5", "1")
    # s.add_one_option ("USER", "KK6", "fadad")


    # print (s.read_section_to_dict ("USER"))

    # print (s.read_section_to_dict ("USER"))
    # print(s.options("LOG"))
    # print(s.read_section_to_dict("LOG"))
    # s.add_one_option("LOG","SECC","1")
    # s.do_action ()
    s.get("EXCEL",'logsn')