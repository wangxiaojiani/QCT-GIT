# -*- coding: utf-8 -*-
#@Time      :2020/7/8    0:51
#@Author    :xj
#@Email     :1027867874@qq.com
#@File      :11.py
#@Software  :PyCharm
import jsonpath
import json

jsonStr = '''
          {
    "lemon": {
        "teachers": [
            {
                "id": "101",
                "ageid":"66",
                "name": "华华",
                "addr": "湖南长沙",
                "age": 25
            },
             {
                "id": "102",
                "name": "韬哥",
                "age": 28
            },
            {
                "id": "103",
                "name": "Happy",
                "addr": "广东深圳",
                "age": 16
            },
             {
                "id": "104",
                "name": "歪歪",
                "addr": "广东广州",
                "age": 29
            }
        ],
        "salesmans": [
            {
                "id": "105",
                "name": "毛毛",
                "age": 17
            },
             {
                "id": "106",
                "name": "大树",
                "age": 27
            }
        ]
    },
 "avg": 25
}
'''

# 3：加载json字符串为json对象
json_obj = json.loads(jsonStr)

# 4：使用jsonpath模块的jsonpath方法提取信息
# eg1： 提取所有包含addr属性的老师信息，结果为list类型
results = jsonpath.jsonpath(json_obj,"$..id")
print(results)
print('hah')
s='6.45'
print(round(float(s)))
