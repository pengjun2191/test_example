import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pj_function.get_config import get_config
from common.KT_op_remote import Paramiko_ssh
from pj_function.op_kt_log import query_log
from datetime import datetime

class get_kt_log:
    def __init__(self) -> None:
        cfg=get_config()
        self.server=cfg.Server
        self.date_day=datetime.date(datetime.now()).strftime("%Y%m%d")[2:]
    def get_log(self,file_name):
        pk_ssh=Paramiko_ssh(self.Server)
        result=pk_ssh.sshop_cmd(query_log(file_name,"check finish")) 
        return result     
    def get_ac_log(self):
        file="ac.log.resource-check."+self.date_day
        ac_log=self.get_log(file)
        return ac_log
    def get_cfgversion_log(self):
        pass
    def get_busicomm_log(self):
        pass
    def get_spliter_log(self):
        pass
    def get_dipatcher_log(self):
        pass
if __name__=="__main__":
    from datetime import datetime
    print("ac.log.resource-check."+datetime.date(datetime.now()).strftime("%Y%m%d")[2:])