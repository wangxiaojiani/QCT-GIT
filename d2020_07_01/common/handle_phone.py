# -*- coding: utf-8 -*-
#@Time      :2020/7/4    1:23
#@Author    :xj
#@Email     :1027867874@qq.com
#@File      :handle_phone.py
#@Software  :PyCharm
import random
from d2020_07_01.common.handle_db import HandleDb
from d2020_07_01.common.myconfig import cnf
from d2020_07_01.common.handle_request import MyRequest

old_user=cnf.read_section_to_dict('PHONE')

#随机生成11位数手机号码
def generate_phone():
    second = [3,5,7,8][random.randint(0,3)] #[3,4,5,6,7,8,9] 正常的数据是这样的 这里为了适应项目调整一下
    third ={3:random.randint(0,9),
            4:[5,7,9][random.randint(0,2)],
            5:[i for i in range(0,10) if i !=4][random.randint(0,8)],
            6:6,
            7:[i for i in range(0,10) if i not in [4,9]][random.randint(0,7)],
            8:random.randint(0,9),
            9:[1,9][random.randint(0,1)]
            }[second]
    other_eight = random.randint(10000000,99999999)
    return int("1{}{}{}".format(second,third,other_eight))

#检验注册表中是否存在这个手机号
def check_phone():
    db = HandleDb()
    while True:
        phone=generate_phone()
        count=db.get_count("""SELECT * FROM member WHERE mobile_phone = {}""".format(phone))
        if count == 0: # 如果手机号不在数据库中，则表示未进行注册过
            break
    return phone


# 登录时需要使用的手机号
def get_old_phone():
    user = old_user['mobile']
    pwd = old_user['pwd']
    MyRequest('post','/futureloan/member/register',{"mobile_phone":user,"pwd":pwd}).send_requests()
    return user,pwd

# 管理员登录使用的手机号码
def admin_old_phone():
    admin_user =old_user['admin_phone']
    admin_pwd = old_user['admin_pwd']
    MyRequest ('post', '/futureloan/member/register', {"mobile_phone": admin_user, "pwd": admin_pwd}).send_requests ()
    return admin_user,admin_pwd


if __name__ == '__main__':
    user, pwd = get_old_phone ()
    res = MyRequest ('POST', '/futureloan/member/login', {"mobile_phone": user, "pwd": pwd}).send_requests ()
    print(res)
    import jsonpath
    s=jsonpath.jsonpath(res.json(),'$..token')
    print(s)