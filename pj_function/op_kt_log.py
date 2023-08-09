import sys,os
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
from common.KT_op_remote import Paramiko_ssh 
from pj_function.get_config import get_config
class op_ktlog:
    def __init__(self) -> None:
        cfg=get_config()
        self.pk_ssh=Paramiko_ssh(cfg.Server)   
    #查询日志
    def grep_log(self,logfilepattern,keywords,path="",grep_type="")->str:
        if path=='':
            quere_log_str=f"cd $HOME;cd log;grep {keywords} {logfilepattern};"
        else:
            quere_log_str=f"cd $HOME;cd log/{path};grep {grep_type} {keywords} {logfilepattern}"
        return self.pk_ssh.sshop_cmd(quere_log_str)
    def grep_spliter_log(self,logfilepattern,keywords,process_name=""):
        if process_name=='':
            self.grep_log(logfilepattern,keywords,"spliter","-R")
        else:
            self.grep_log(logfilepattern,keywords,f"spliter/{process_name}")
   
    def grep_busicomm_log(self,logfilepattern,keywords,process_name=""):
        if process_name=='':
            self.grep_log(logfilepattern,keywords,"busicomm","-R")
        else:
            self.grep_log(logfilepattern,keywords,f"busicomm/{process_name}")
    
    def grep_dispatcher_log(self,logfilepattern,keywords,process_name=""):
        if process_name=='':
            self.grep_log(logfilepattern,keywords,"dispatcher","-R")
        else:
            self.grep_log(logfilepattern,keywords,f"dispatcher/{process_name}")

   #删除日志 
    def del_app_log(self,path='',deltype=''):
        if path=='':
            del_app_log_str="cd $HOME;cd log;rm *;"
        else:
            del_app_log_str=f"cd $HOME;cd log/{path};rm {deltype} *;"
        self.pk_ssh.sshop_cmd(del_app_log_str)
    def del_spliter_log(self,process_name=''):
        if process_name=='':
            self.del_app_log("spliter","-rf")
        else:
            self.del_app_log(f"spliter/{process_name}")
    def del_busicomm_log(self,process_name=''):
        if process_name=='':
            self.del_app_log("busicomm","-rf")
        else:
            self.del_app_log(f"busicomm/{process_name}")

    def del_dispatcher_log(self,process_name=''):
        if process_name=='':
            self.del_app_log("dispatcher","-rf")
        else:
            self.del_app_log(f"dispatcher/{process_name}")

if __name__=="__main__":
    op_ktlog().del_busicomm_log()