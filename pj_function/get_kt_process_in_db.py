import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pj_function.get_config import get_config
from common.KT_op_antdb  import OpAntDB 

class get_process_info:
    def __init__(self) -> None:
        cfg=get_config()
        self.ip=cfg.appControl_cfg['appControl_ip']
        self.port=cfg.appControl_cfg['appControl_port']
        self.antdb=cfg.AntDBTest
        
    def op_sql(self,sqls):
        opdb=OpAntDB(self.antdb)
        try:
            opdb.im_db(sqls)
            content=opdb.op_db_all()
            opdb.cl_db()
            return content
        except Exception as e:
            print (e)
    
    def get_process_name_by_machine_name(self):
        sql=f"select smp.process_name from sys_machine_process smp where smp.state=1 and smp.machine_name=(select rg.machine_name from  rpc_register rg where rg.rpc_ip='{self.ip}' and  rg.rpc_port='{self.port}') order by sort;"
        process_name=self.op_sql(sql)
        return process_name
    
    def get_process_type_by_process_name(self,process_name):
        sql=f"select process_type from sys_process where process_name='{process_name}';"
        process_type=self.op_sql(sql)
        return process_type
    
    def get_group_name_by_process_type(self,process_type): 
        sql=f"select app_group_name from sys_process_type where process_type='{process_type}';"
        app_group_name=self.op_sql(sql)
        return app_group_name
    
    def get_process_name_by_process_type(self,process_type):
        sql=f"select smp.process_name from sys_machine_process smp ,sys_process sp where smp.state=1 and smp.machine_name=(select rg.machine_name from  rpc_register rg where rg.rpc_ip='{self.ip}' and  rg.rpc_port='{self.port}') and sp.process_name=smp.process_name and sp.process_type='{process_type}';"
        process_name=self.op_sql(sql)
        return process_name
    
    def get_RT_split_in_proxy_route(self):
        sql="select process_name from ps_proxy_route ppr  where ppr.type =3"
        RT_split_list=self.op_sql(sql)
        return RT_split_list
    
    def get_normal_split_in_proxy_route(self):
        sql="select process_name from ps_proxy_route ppr  where ppr.type =1"
        normal_split_list=self.op_sql(sql)
        return normal_split_list
    
    def get_busicomm_name(self):
        return self.get_process_name_by_process_type("busicomm")
    
    def get_normal_spliter_name(self):
        normal_spliter_name=[]
        for process_name in self.get_process_name_by_process_type("spliter"):
            if (process_name[0],) in self.get_normal_split_in_proxy_route():
                normal_spliter_name.append(process_name)
        return normal_spliter_name
    
    def get_RT_spliter_name(self):
        RT_spliter_name=[]
        for process_name in self.get_process_name_by_process_type("spliter"):
            if process_name in self.get_RT_split_in_proxy_route():
                RT_spliter_name.append(process_name)
        return RT_spliter_name
    
    def get_dispatch_name(self):
        return self.get_process_name_by_process_type("dispatcher")
    
    def get_cfgversion_name(self):
        return self.get_process_name_by_process_type("cfgversion")
    
if __name__=="__main__":
    print(get_process_info().get_normal_spliter_name()[0][0])
