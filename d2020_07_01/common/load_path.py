# -*- coding: utf-8 -*-
#@Time      :2020/6/17    22:45
#@Author    :xj
#@Email     :1027867874@qq.com
#@File      :load_path.py
#@Software  :PyCharm


import os

# 当前文件路径
current_file_path = os.path.abspath(__file__)

# 获取当前文件所在模块路径
current_file_dir_path = os.path.dirname(current_file_path)

# 获取项目工程目录
curent_project_path = os.path.split(current_file_dir_path)[0]

# 测试用例加载路径
load_test_path = os.path.join(curent_project_path,"test_cases")

# 测试报告路径
load_test_report_path =os.path.join(curent_project_path,"report_html")

# excel测试数据目录
load_data_path = os.path.join(curent_project_path,"test_data","nmb_qcd.xlsx")

# log日志路径
load_log_path = os.path.join(curent_project_path,"log","my_log.log")

# 配置文件路径
load_ini_path = os.path.join(curent_project_path,"config","myconfig.ini")