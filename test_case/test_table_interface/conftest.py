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
from pj_function.op_kt_process import op_ktprocess
from common.KT_op_antdb  import OpAntDB as opdb
import pytest
from pj_function.get_kt_table_info import get_table_info


get_t_info=get_table_info()
cfg_db=get_config()
data=[{}]
data[0]["file"]=cfg_db.TestData["file"]
data[0]["configdb"]=cfg_db.AntDBTest
data[0]["table_names"]=cfg_db.tablename["interfacetable"]+cfg_db.tablename["histable"]


@pytest.fixture(scope='class',params=data,autouse=True)
@pytest.mark.parametrize("file,configdb,table_names",data)
def init_i_data(request):
	print("清理关闭测试进程")
	op_kt=op_ktprocess()
	if op_kt.get_app_start_num()>0:
		op_kt.shutdown_all()
	print("清理测试进程完成")
	print("初始化插入数据到i表")
	db=opdb(request.param["configdb"])
	for table_name in request.param["table_names"]:
		sql=delete_table(table_name)
		db.im_db(sql)
		db.im_commit()
	opExcel=OpExcel(request.param["file"])
	table_dict=opExcel.get_data()
	for key in table_dict.keys():
		sql,data=insert_table(key,table_dict[key])
		db.im_db_many(sql,data)
	db.im_commit()
	db.cl_db()
	print("开始插入数据到i表结束")

	yield
	print("开始清理数据")
	db=opdb(request.param["configdb"])
	for table_name in request.param["table_names"]:
		sql=delete_table(table_name)
		db.im_db(sql)
	db.im_commit()
	db.cl_db()		


if __name__=='__main__':
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