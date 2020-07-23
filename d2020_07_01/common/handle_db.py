# -*- coding: utf-8 -*-
#@Time      :2020/7/3    22:37
#@Author    :xj
#@Email     :1027867874@qq.com
#@File      :handle_db.py
#@Software  :PyCharm

import pymysql
from d2020_07_01.common.myconfig import cnf
db_cnf =cnf.read_section_to_dict("DB")

class HandleDb(object):
    def __init__(self):

        self.cnn = pymysql.connect(host=db_cnf["host"],
                                   user=db_cnf["user"],
                                   port=db_cnf["port"],
                                   password=db_cnf["password"],
                                   database=db_cnf["database"],
                                   charset="utf8",
                                   cursorclass=pymysql.cursors.DictCursor) # cursorclass 声明读取出来的数据为字典格式 最外层为列表 如果不设置该参数每行返回数据是元组类型，最外层也是元组

        self.cur =self.cnn.cursor()

    def select_one_data(self,sql):
        try:
            self.cnn.commit () # 查询之前先commit 同步最新数据库数据
            self.cur.execute(sql)
            data = self.cur.fetchone()
        except Exception:
            print("fetchone获取数据失败")
            raise
        return data # 获取格式为{}类型  获取不到时为None

    def select_all_data(self,sql):
        try:
            self.cnn.commit ()
            self.cur.execute(sql)
            all_data=self.cur.fetchall()
        except Exception:
            print("fetchall获取数据失败")
            raise
        return all_data # 获取格式为[{},{}]  获取不到数据时为空列表

    def get_count(self,sql):
        try:
            self.cnn.commit ()
            num=self.cur.execute(sql)
        except Exception:
            print("sql语句错误，影响行数获取失败")
            raise
        return num # 查不到结果 返回0

    def update_data(self,sql):
        try:
            self.cur.execute(sql)
            self.cnn.commit()
        except Exception:
            self.cnn.rollback()
            print("更新数据异常，事务进行回滚")
            raise


    def db_close(self):
        self.cur.close()
        self.cnn.close()
if __name__ == '__main__':
    from decimal import *
    db=HandleDb()
    # sql ="""select cast(leave_amount as CHAR) AS leave_amount from member WHERE id =220261;"""
    sql = """select leave_amount AS leave_amount from member WHERE id =22044461;"""
    s=db.get_count(sql)
    print(s)
    # s=db.select_all_data(sql)
    # p=s[0]['leave_amount']
    # s=p.quantize(Decimal('0.000'))
    #
    #
    # print(type(s))
    db.db_close()

