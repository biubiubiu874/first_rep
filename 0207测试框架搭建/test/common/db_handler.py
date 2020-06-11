# -*- coding:utf-8 -*-
# _author_='lijiachang'
# @time :2020/2/23 11:14

import pymysql
from pymysql.cursors import DictCursor
class DBHandler:
#可以将数据库等信息写到配置文件中 方便管理
    def __init__(self,host='120.78.128.25', port=3306,
                               user='future', password='123456',
                               charset='utf8', database='futureloan',
                               cursorclass=DictCursor,**kwargs):
        #初始化
        # TODO:utf-8  要写成utf8
        self.conn = pymysql.connect(host=host, port=port,
                               user=user, password=password,
                               charset=charset, database=database,
                               cursorclass=cursorclass,**kwargs

                               )
        # 游标
        self.cursor = self.conn.cursor()

    def query(self,sql,args=None,one=True):
        # args，%s占坑符  需要元祖  列表
        self.cursor.execute(sql, args)
        #提交事务
        self.conn.commit()
        # 获取游标结果
        if one:
            return self.cursor.fetchone()
        else:
            return self.cursor.fetchall()
        self.conn.commit()
        # two = cursor.fetchmany(size=2)

    def close(self) -> object:
        self.cursor.close()
        self.conn.close()
if __name__ == '__main__':
    db=DBHandler()
    querymoney = db.query('SELECT * from member where id=%s;', args=[9584714])
    print(querymoney)








