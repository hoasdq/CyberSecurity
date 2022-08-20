# !/usr/bin/python
# -*- coding: UTF-8 -*-

import pymysql
from pymysql.cursors import DictCursor

class LogMysql():
    def __init__(self):
        #数据库不一样的要改一下
        self.con=pymysql.connect(host='localhost',user='root',password='123456',port=3306,database='log',charset='utf8',autocommit=True) 
        self.cursor1=self.con.cursor(cursor=DictCursor)
        # self.cursor1.execute(query="show databases")
        # print(self.cursor1.execute(query="show databases")) #打印个数
        # results=self.cursor1.fetchall()
        # print(results) #列表里存着字典
        # self.insert1('1','2','3','4','5')
 
            
    def insert1(self,did,rid,match,description,level):
        # sql_str = 'insert into logs(did,rid,logmatch,description,loglevel) values(%s,%s,%s,%s,%s) '% (repr(did),repr(rid),repr(match),repr(description),repr(level))
        sql_str=f'insert into logs(did,rid,logmatch,description,loglevel)  values({repr(did)},{repr(rid)},{repr(match)},{repr(description)},{repr(level)});'
        self.cursor1.execute(sql_str)
        # self.con.commit() #注释掉,连接数据库带上autocommit=True参数
        # self.con.close()
        # self.cursor1.close()


    # def insert2(self,did,rid,match,description,level):
        # sql_str=f'insert into logs(did,rid,logmatch,description,loglevel)  values({repr(did)},{repr(rid)},{repr(match)},{repr(description)},{repr(level)});'
        # self.cursor1.execute(sql_str)




# logMysql=LogMysql()
