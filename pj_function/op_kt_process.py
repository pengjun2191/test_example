""" 子进程
    app_spliter|spliter|SPLIT_A_ANTDB
    app_spliter|spliter|SPLIT_RT_AUTO_ANTDB
    app_dispatcher|dispatcher|DISPATCH_A_ANTDB
    app_ne|busicomm|NE_AUTO_ANTDB
    app_common|cfgversion|VERSION_AUTO_ANTDB
    app_common|cfgdebug|DEBUG_AUTO_ANTDB
 """
""" 
count_numapp=`ps -ef |grep appControl |grep -v "grep"|wc -l`
count_onlyapp=`ps -ef |grep $appfile_name |grep -v "grep"|wc -l`
count_rpc=`ps -ef |grep RPC |grep -v "grep"|wc -l` 
"""
import sys,os
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from common.KT_op_remote import Paramiko_ssh 
from pj_function.get_config import get_config


class op_ktprocess:
    def __init__(self) -> None:
        cfg=get_config()
        self.pk_ssh=Paramiko_ssh(cfg.Server)
        self.ip=cfg.appControl_cfg['appControl_ip']
        self.port=cfg.appControl_cfg['appControl_port']
        self.cfgfile=cfg.appControl_cfg['cfgfile']

    def get_run_process(self,pattern):
        get_run_info=f"""ps -ef |grep {pattern}|grep -v "grep"|awk '{{print $2}}'"""
        return self.pk_ssh.sshop_cmd(get_run_info).strip("\n")  
    
    def get_process_run_num(self,pattern):
        get_info=f"""ps -ef |grep {pattern}|grep -v "grep"|grep {self.get_appControl()}|wc -l""" 
        return int(self.pk_ssh.sshop_cmd(get_info)) 
    def get_app_start_num_by_process_name(self,process_name):
        return self.get_process_run_num(process_name)             
    def get_app_start_num(self):
        return self.get_process_run_num("appControl")
    def get_cfgversion_start_num(self):
        return self.get_process_run_num("cfgversion")   
    def get_dispatch_start_num(self):
        return self.get_process_run_num("dispatcher")
    def get_spliter_start_num(self):
        return self.get_process_run_num("spliter")
    def get_busicomm_start_num(self):
        return self.get_process_run_num("busicomm")

    def get_appControl(self):
        return self.get_run_process(self.cfgfile)
    
    def get_rpc(self):
        get_rpc=f"""ps -ef |grep RPC |grep -v "grep"|grep {self.get_appControl()}|awk '{{print $2}}'"""
        return self.pk_ssh.sshop_cmd(get_rpc)

    def start_all(self)->str:
        #cfgpath 为配置文件绝对路径
        start_allstr=f"cd $HOME;cd bin;nohup appControl -ai ../config/{self.cfgfile} >/dev/null &;exit\n"
        return self.pk_ssh.sshop_cmd(start_allstr)
    
    def kill_excption_process(self,process_name)->str:
        kill_all=f"""ps -ef |grep {process_name} |grep -v "grep"|awk '{{print $2}}'|xargs -r kill -9 """
        return self.pk_ssh.sshop_cmd(kill_all)
    
    def kill_excption_busicomm(self)->str:
        return self.kill_excption_process("busicomm")
    
    def kill_excption_dispatcher(self)->str:
        return self.kill_excption_process("dispatcher")
    
    def kill_excption_spliter(self)->str:
        return self.kill_excption_process("spliter")
    
    def kill_excption_cfgversion(self)->str:
        return self.kill_excption_process("cfgversion")

    def shutdown_all(self)->str:
        return self.kill_excption_process(self.get_appControl())
    
    def start_appControl(self)->str:
        #cfgpath 为配置文件绝对路径
        start_allstr=f"cd $HOME;cd bin;nohup appControl -i ../config/{self.cfgfile} >/dev/null &;exit\n"
        return self.pk_ssh.sshop_cmd(start_allstr)
    
    def shutdown_appControl(self)->str:
        kill_app=f"""ps -ef |grep {self.cfgfile}|grep -v "grep"|awk '{{print $2}}'|xargs -r kill -9"""
        kill_rpc="""ps -ef |grep RPC |grep -v "grep"|awk '{print $2}'|xargs -r kill -9"""
        kill_content=[kill_rpc,kill_app]
        return self.pk_ssh.sshop_more_cmd(kill_content)

    def op_sub_process(self,cmd,app_group_name,process_type,process_name):
        op_sub_process=f"""cd $HOME;cd bin;
        appControl -c {self.ip}:{self.port}<<EOF
        {cmd} {app_group_name}|{process_type}|{process_name}
        exit
        kill -s SIGINT
        EOF"""
        return self.pk_ssh.sshop_cmd(op_sub_process)
    
    def start_cfgversion(self,process_name)->str:
        start_str=self.op_sub_process("startup","app_common","cfgversion",process_name)
        return start_str
    
    def shutdown_cfgversion(self,process_name)->str:
        shutdown_str=self.op_sub_process("shutdown","app_common","cfgversion",process_name)
        return shutdown_str
    
    def start_dispatch(self,process_name)->str:
        start_str=self.op_sub_process("startup","app_dispatcher","dispatcher",process_name)
        return start_str
    
    def shutdown_dispatch(self,process_name)->str:
        shutdown_str=self.op_sub_process("shutdown","app_dispatcher","dispatcher",process_name)
        return shutdown_str
    
    def start_split(self,process_name)->str:
        start_str=self.op_sub_process("startup","app_spliter","spliter",process_name)
        return start_str
    
    def shutdown_split(self,process_name)->str:
        shutdown_str=self.op_sub_process("shutdown","app_spliter","spliter",process_name)
        return shutdown_str
    
    def start_busicomm(self,process_name)->str:
        start_str=self.op_sub_process("startup","app_ne","busicomm",process_name)
        return start_str
    
    def shutdown_busicomm(self,process_name)->str:
        shutdown_str=self.op_sub_process("shutdown","app_ne","busicomm",process_name)
        return shutdown_str
    


    

if __name__=="__main__":
    def start():
        op_kt=op_ktprocess()
        num=op_kt.get_app_start_num()
        print (num)
        if num==0:
            print('startall')
            result=op_kt.start_all()
        elif num>0 and num!=10:
            op_kt.shutdown_all()
            op_kt.start_all()
    start()
    import get_kt_process_in_db
    op_kt=op_ktprocess()
    op_kt.get_appControl()
    get_process=get_kt_process_in_db.get_process_info()
    for split_name in get_process.get_cfgversion_name():
        print(split_name[0])
        #op_kt.shutdown_split(split_name[0])
        #op_kt.start_split(split_name[0])