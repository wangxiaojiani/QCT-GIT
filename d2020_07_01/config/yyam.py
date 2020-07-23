# -*- coding: utf-8 -*-
#@Time      :2020/6/20    14:07
#@Author    :xj
#@Email     :1027867874@qq.com
#@File      :yyam.py
#@Software  :PyCharm

import yaml

fp = open("nmb.yaml",encoding="utf-8")
S=yaml.load(fp,yaml.FullLoader) # 输出字典
print(S['passwd'])
print(type(S['passwd']))
