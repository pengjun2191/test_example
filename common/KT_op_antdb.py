import psycopg2 as mdb
from psycopg2 import extras
import common.KT_base_dbop as OpDbBase

class OpAntDB(OpDbBase.OpDb):
    def __init__(self,configdb):
        self.dbip = configdb['dbhost']
        self.dbport = configdb['dbport']
        self.dbname = configdb['dbname']
        self.dbuser = configdb['dbuser']
        self.dbpwd = configdb['dbpassword']
        self.cursor=None
        self.conn=None

    def conn_db(self):
        try:
            self.conn = mdb.connect(database=self.dbname,user=self.dbuser,password=self.dbpwd,host=self.dbip,port=self.dbport)
        except mdb.Error as e:
            print("Unable to connect!")
            return e
        else:
            return True

    def cus_db(self):
        if self.conn is not None:
            if self.cursor is not None:
                return True
            else:
                self.cursor = self.conn.cursor()
                if self.cursor is not None:
                    return True
                else:
                    return False

    #操作数据库
    def op_db(self):
        #获取查询出来的未被获取的第一条数据
        result=self.cursor.fetchone()
        return result

    def op_db_many(self,n):
        #指定获取n条查询出来的未被获取的数据
        result=self.cursor.fetchmany(n)
        return result
          
    def op_db_all(self):
        #获取查询出来的未被获取的所有数据
        result=self.cursor.fetchall()
        return result
    def op_db_all_add_colums(self):
        #得到查询的列名
        cols=self.cursor.description
        result = self.op_db_all()
        col_names=[]
        for i in range(len(cols)):
            col_names.append(cols[i][0])
        result.insert(0,tuple(col_names))
        return result

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
                extras.execute_values(self.cursor,sqls,values)
            except Exception as e:
                print("执行AntDB: %s %s时出错:%s"%(sqls,values,e))

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
                self.cursor.execute(sqls)
            except Exception as e:
                print ("执行AntDB: %s 时出错:%s"%(sqls , e))

    def im_db_file(self,sqls_file):
        if self.conn is not None:
            self.cus_db()
        else:
            self.conn_db()
            if self.conn is not None:
                self.cus_db()
            else:
                return False
        if sqls_file is not None:
            try:
                content=open(sqls_file, "r",encoding='utf-8')
                values=content.read()
                self.cursor.execute(values)
                content.close()
            except Exception as e :
                print("执行AntDB: %s %s时出错:%s"%(sqls_file,values,e))

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