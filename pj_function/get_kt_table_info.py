import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from common.KT_op_antdb  import OpAntDB
from pj_function.get_config import get_config
from pj_function.op_kt_table import  query_his

class get_table_info:
    def __init__(self) -> None:
        cfg=get_config()
        self.db_config=cfg.AntDBTest
        self.tablenames=cfg.tablename["histable"]+cfg.tablename["interfacetable"]
        self.content={}
        
    def get_table_count(self,table,**keyword):
        opdb=OpAntDB(self.db_config)
        sql=query_his(table,['count(*)'],keyword)
        opdb.im_db(sql)
        self.content[table]=opdb.op_db()
        opdb.cl_db()
        return self.content
    def get_table_alldata(self,**keyword):
        opdb=OpAntDB(self.db_config)
        for table in self.tablenames:
            sql=query_his(table,['*'],keyword)
            opdb.im_db(sql)
            self.content[table]=opdb.op_db_all_add_colums()
        opdb.cl_db()
        return self.content

    def i_table_count(self):
        return self.get_table_count('i_provision_931')['i_provision_931']
    def i_table_his_count(self):
        return self.get_table_count('i_provision_his_931_202307')['i_provision_his_931_202307']
    def ps_table_count(self):
        return self.get_table_count('ps_provision_931')['ps_provision_931']
    def ps_table_his_count(self):
        return self.get_table_count('ps_provision_his_931_202307')['ps_provision_his_931_202307']
    def split_table_count(self):
        return self.get_table_count('ps_provision_split_931')['ps_provision_split_931']
    def split_table_his_count(self):
        return self.get_table_count('ps_split_his_931_202307')['ps_split_his_931_202307']
    def reset_table_count(self):
        return self.get_table_count('i_ps_provision_reset_931')['i_ps_provision_reset_931']
    def common_store_count(self):
        return self.get_table_count('PS_DIRECTRESP_STORE_931_202307')['PS_DIRECTRESP_STORE_931_202307']
    #查询状态为0的工单
    def i_table_count_status_init(self):
        return self.get_table_count('i_provision_931',ps_status=0)['i_provision_931']
    def ps_table_count_status_init(self):
        return self.get_table_count('ps_provision_931',ps_status=0)['ps_provision_931']
    def split_table_count_status_init(self):
        return self.get_table_count('ps_provision_split_931',ps_status=0)['ps_provision_split_931']
    #查询状态为1的工单
    def i_table_count_status_running(self):
        return self.get_table_count('i_provision_931',ps_status=1)['i_provision_931']
    def ps_table_count_status_running(self):
        return self.get_table_count('ps_provision_931',ps_status=1)['ps_provision_931']
    def split_table_count_status_running(self):
        return self.get_table_count('ps_provision_split_931',ps_status=1)['ps_provision_split_931']
    #查询成功的工单
    def ps_table_his_count_status_success(self):
        return self.get_table_count('ps_provision_his_931_202307',ps_status=9)['ps_provision_his_931_202307']
    def split_table_his_count_status_success(self):
        return self.get_table_count('ps_split_his_931_202307',ps_status=9)['ps_split_his_931_202307']
    #查询失败的工单
    def ps_table_his_count_status_fail(self):
        return self.get_table_count('ps_provision_his_931_202307',ps_status=-1)['ps_provision_his_931_202307']
    def split_table_his_count_status_fail(self):
        return self.get_table_count('ps_split_his_931_202307',ps_status=-1)['ps_split_his_931_202307']



if __name__=="__main__":
    get_t_info=get_table_info()
    print(get_t_info.get_table_alldata())