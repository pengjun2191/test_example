import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from common.KT_op_configfile import  Config_yaml as yaml ,Project as cfg

class get_config:
    def __init__(self):
        self.TestData=None
        self.AntDBDev=None
        self.AntDBServer=None
        self.Server=None
        self.AntDBTest=None
        self.appControl_cfg=None
        self.test_report_dir=None
        self.init_db=None
        self.tablename=None
        self.webserviceurl=None
        self.httpurl=None
        self.yaml_file="./config/config.yml"
        self.cfg_file="./config/useconfig.cfg"
        self.config_cfg()
        self.config_yml()
    def config_cfg(self):
        cfg_parse=cfg()
        self.AntDBTest=cfg_parse.Useproject("./config/useconfig.cfg","AntDBTest")["AntDBTest"]
        self.appControl_cfg=cfg_parse.Useproject("./config/useconfig.cfg","appControl_cfg")["appControl_cfg"]
        self.test_report_dir=cfg_parse.Useproject("./config/useconfig.cfg","test_report_dir")["test_report_dir"]
        self.Server=cfg_parse.Useproject("./config/useconfig.cfg","Server")["Server"]
        self.init_db=cfg_parse.Useproject("./config/useconfig.cfg","init_db")["init_db"]
    def config_yml(self):
        db_yaml=yaml()
        section_all=db_yaml.config_yaml("./config/config.yml")
        self.TestData=section_all["TestData"]
        self.AntDBDev=section_all["AntDBDev"]
        self.AntDBServer=section_all["AntDBServer"]
        self.tablename=section_all["db_table"]
        self.webserviceurl=section_all["sync_interface"]
        self.httpurl=section_all["http_interface"]

cfg_singleton=get_config()
if __name__=="__main__":
    cfg=get_config()
    print(cfg.webserviceurl["webservice"])