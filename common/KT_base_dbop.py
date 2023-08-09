# -*- coding: utf8 -*-
class OpDb:
    def __init__(self):
        '''
        对象初始化

        获取本地化数据库连接所需要的信息,数据库的Ip、Port、数据库名称、登录用户、登录密码相关信息
        '''
        pass

    def conn_db(self):
        '''
        创建数据库连接对象
        连接成功返回true,失败返回false
        '''
        pass

    def cus_db(self):
        '''
        创建一个数据库游标对

        返回值:链接对象创建成功返回True、失败返回False
        '''
        pass

    def op_db_all(self):
        '''
        操作数据库,可进行查询,返回全部结果
        '''
        pass

    def op_db(self):
        '''
        查询返回单条记录
        '''
        pass

    def im_db_many(self):
        '''
        批量执行sql,executemany
        '''
        pass
    def im_db(self):
        '''
        .sql文件导入,execute
        '''
        pass

    def cl_db(self):
        '''
        关闭数据库连接
        '''
        pass

    def im_commit(self):
        '''
        提交
        '''
        pass

    def im_rollback(self):
        '''
        回滚
        '''
        pass
