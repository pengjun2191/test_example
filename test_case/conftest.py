""" 
conftest.py 文件名是固定的，不能更改
一般情况下将conftest.py文件放在管理用例的包下面
不同目录可以有自己的conftest.py，一个项目中可以有多个conftest.py
pytest会默认读取conftest.py里面的所有fixture
测试用例文件中不需要手动import conftest.py 或 from ... import conftest.py
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from common.KT_op_excel import OpExcel
from pj_function.op_kt_table import  insert_table,delete_table
from pj_function.get_config import get_config
from common.KT_op_antdb  import OpAntDB as opdb
import pytest
import pj_function.kt_init_antdb as kt_init
from pj_function.get_kt_table_info import get_table_info

@pytest.fixture(scope='session',autouse=True)
def init_db():
	kt_init.init()


if __name__=='__main__':
	get_t_info=get_table_info()
	cfg_db=get_config()
	opExcel=OpExcel(cfg_db.TestData["file"])
	table_dict=opExcel.get_data()
	for key in table_dict.keys():
		sql,data=insert_table(key,table_dict[key])
		db=opdb(cfg_db.AntDBTest)
		db.im_db_many(sql,data)
	db.im_commit()
	db.cl_db()
	""" 	
	from pj_function.op_antdb_process import op_antdb_process
	op_antdb=op_antdb_process()
	op_antdb.antdb_net_break()
	op_antdb.antdb_iptables_break()
	op_antdb.antdb_firewall_break() """