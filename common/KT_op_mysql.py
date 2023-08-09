# -*- coding: utf8 -*-
import pymysql as mdb
import KT_base_dbop as OpDbBase
import sys
sys.setdefaultencoding('utf-8')
import logging
logger = logging.getLogger("main.Mysql")

class OpDbMysql(OpDbBase.OpDb):
    def __init__(self,configdb):
        self.dbip = configdb['dbhost']
        self.dbport = configdb['dbport']
        self.dbname = configdb['dbname']
        self.dbuser = configdb['dbuser']
        self.dbpwd = configdb['dbpassword']
        
    # 连接数据库
    def conn_db(self): 
        try:
            self.conn = mdb.connect(host=self.dbip,user=self.dbuser,passwd=self.dbpwd,db=self.dbname,port=int(self.dbport),charset="utf8")
            return True
        except Exception as e:
            return e
    # 获取游标
    def cus_db(self):
        if self.conn is not None:
            self.cursor = self.conn.cursor()
            if self.cursor is not None:
                return True
            else:
                return False
    #操作数据库
    def op_db(self):
        result=self.cursor.fetchone()
        return result

    def op_db_many(self,n):
        #指定获取n条查询出来的未被获取的数据
        result=self.cursor.fetchmany(n)
        return result
          
    def op_db_all(self):
        result=self.cursor.fetchall()
        return result
        
    def get_names(self):
        #返回查询的字段名
        names=[]
        for hotelrs in self.cursor.description:
            names.append(hotelrs[0])
        return names

    def im_db_many(self,sqls,values):
        if self.conn is not None:
            self.cus_db()
        else:
            self.conn_db()
            if self.conn is not None:
                self.cus_db()
            else:
                return False
        if values is not None:
            try:
                self.cursor.executemany(sqls,values)
            except Exception as e:
                print ("执行MySQL: %s %s时出错:%s"%(sqls,values,e))


    def im_db(self,sqls):
        if self.conn is not None:
            self.cus_db()
        else:
            self.conn_db()
            if self.conn is not None:
                self.cus_db()
            else:
                return False
        if sqls is not None:
            try:
                count=self.cursor.execute(sqls)
                return count
            except Exception as e:
                print (u"执行MySQL: %s 时出错:%s"%(sqls, e))

    def cl_db(self):
        try:
            self.cursor.close()
            self.conn.close()
        except:
            pass
        return True

    def im_commit(self):
        try:
            self.conn.commit()
            return True
        except Exception as e:
            return e

    def im_rollback(self):
        try:
            self.conn.rollback()
        except Exception as e:
            return e