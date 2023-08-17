import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from common.KT_op_antdb  import OpAntDB as opdb
from pj_function.get_config import cfg_singleton as cfg
from common.KT_base_dbop import OpDb

#adb_conn="dbname=jfjs user=settle password=settle0328 host=10.19.93.73 port=5432"
#adb_conn="dbname=testdb1 user=user1 password=456@789@321 host=10.19.14.34 port=5432"
#执行目录下sql文件到数据库
def init_db(db:OpDb,init_db_path,endwithstr=".sql"):
    try:
        for file_name in os.listdir(init_db_path):
            if str(file_name).endswith(endwithstr) :
                path_name=os.path.join(init_db_path,file_name)
                if os.path.isfile(path_name):
                    print("执行%s开始"%(file_name))
                    db.im_db_file(path_name)
                    print("执行{}结束".format(file_name))
        db.im_commit()
    except:
        db.im_rollback()
    else:
        db.cl_db()

def init():
    init_db_path=cfg.init_db["db_scripts"]
    #初始化进程配置
    db=opdb(cfg.AntDBTest)
    init_db(db,init_db_path)
    #db_yaml=opdb(cfg.AntDBDev)
    #init_db(db_yaml,init_db_path)

     

if __name__ == '__main__':
    init()

    """ 
    db.im_db("update sys_machine_process set state=1 where process_name ='SPLIT_RT_AUTO_ANTDB';")
    db.im_db("update sys_machine_process set state=0 where process_name ='SPLIT_A_ANTDB';")

    db.im_db("update sys_machine_process set state=1 where process_name ='SPLIT_A_ANTDB';")
    db.im_db("update sys_machine_process set state=0 where process_name ='SPLIT_RT_AUTO_ANTDB';")

    db.im_commit()
    db.cl_db() """


    

    
    