""" 
本文件是放置多个测试case共用的测试步骤函数
"""
import sys,os
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import pytest
import allure
import time
import inspect
from pj_function.op_kt_process import op_ktprocess
from pj_function.get_kt_process_in_db import get_process_info
from pj_function.get_kt_table_info import get_table_info
from pj_function.get_config import get_config
from common.KT_op_excel import WtXlsx


cfg=get_config()
get_t_info=get_table_info()
op_kt=op_ktprocess()
get_process=get_process_info()

def table_interface_check_histable(i_table_count_num):
	with allure.step("休眠1200等待恢复连接，进程处理"):
		time.sleep(1200) 
	with allure.step("查看i历史表"):
		i_table_his_num=get_t_info.i_table_his_count()[0]
		allure.attach(f"调度处理到i历史表期望入表{i_table_count_num},实际数量为{i_table_his_num}")
		print(f"i历史表实际数量为{i_table_his_num}")
		pytest.assume(i_table_his_num==i_table_count_num)
	with allure.step("查看ps历史表"):
		ps_table_his_num=get_t_info.ps_table_his_count()[0]
		allure.attach(f"调度处理到ps历史表期望入表{i_table_count_num},实际数量为{ps_table_his_num}")
		print(f"ps历史表实际数量为{ps_table_his_num}")
		pytest.assume(ps_table_his_num==i_table_count_num)
	with allure.step("查看reset表"):
		reset_table_num=get_t_info.reset_table_count()[0]
		allure.attach(f"调度回执处理到reset表期望入表{i_table_count_num},实际数量{reset_table_num}")
		print(f"调度回执处理到reset表的实际数量{reset_table_num}")
		pytest.assume(reset_table_num==i_table_count_num)
	with allure.step("查看split历史表"):
		split_table_his_num=get_t_info.split_table_his_count()[0]
		allure.attach(f"拆分回执处理到split历史表期望入表{i_table_count_num*2},实际数量{split_table_his_num}")
		print(f"拆分回执处理到split历史表的实际数量{split_table_his_num}")
		pytest.assume(split_table_his_num>=i_table_count_num*2)
	with allure.step("查看指令保存表"):
		common_store_num=get_t_info.common_store_count()[0]
		allure.attach(f"启动后网元处理指令期望入表{i_table_count_num*2},入表的实际数量{common_store_num}")
		print(f"启动后网元处理指令入表的实际数量{common_store_num}")
		pytest.assume(common_store_num>=i_table_count_num*2)	
	with allure.step("确认接口表数量"):
		ps_table_num=get_t_info.ps_table_count()[0]
		split_table_num=get_t_info.split_table_count()[0]
		allure.attach(f"父工单表剩余的实际数量{ps_table_num},子工单表剩余的实际数量{split_table_num}")
		print(f"父工单表剩余的实际数量{ps_table_num},子工单表剩余的实际数量{split_table_num}")

def save_data_result():
	file_name=inspect.stack()[1][3]+".xlsx"
	with allure.step("保存数据库表测试结果数据"):
		file_path=os.path.realpath(cfg.test_report_dir["data_result_dir"])
		if not os.path.exists(file_path):
			os.mkdir(file_path)
		file=os.path.join(file_path,file_name)
		if os.path.exists(file):
			os.remove(file)
		save_d_result=WtXlsx(file)
		data_result=get_t_info.get_table_alldata()
		#data_result={'v4command_store_931_20230721': [(1,2,3,4,5,6,7),(1,2,3,4,5,6,7)], 'PS_DIRECTRESP_STORE_931_202307': [(1,2,3,4,5,6,7),(1,2,3,4,5,6,7)], 'ps_split_his_931_202307': [(1,2,3,4,5,6,7),(1,2,3,4,5,6,7)], 'ps_provision_his_931_202307': [], 'i_provision_his_931_202307': [], 'i_provision_931': [], 'ps_provision_931': [], 'ps_provision_split_931': [(1,2,3,4,5,6,7),(1,2,3,4,5,6,7)], 'i_ps_provision_reset_931': [(1,2,3,4,5,6,7),(1,2,3,4,5,6,7)]}
		for key,values in data_result.items():
			sheet=save_d_result.add_sheet(key)
			if values!=[]:
				rows=0
				for value in values:
					save_d_result.write_rows(sheet,rows,0,value)
					rows+=1
		save_d_result.save_file()
		allure.attach.file(file,attachment_type=allure.attachment_type.CSV)

def sync_interface_check_histable(source_ps_num):
	with allure.step("休眠1200等待恢复连接，进程处理"):
		time.sleep(1200) 
	with allure.step("查看split历史表"):
		split_table_his_num=get_t_info.split_table_his_count()[0]
		allure.attach(f"拆分回执处理到split历史表期望入表{source_ps_num*2},实际数量{split_table_his_num}")
		print(f"拆分回执处理到split历史表的实际数量{split_table_his_num}")
		pytest.assume(split_table_his_num>=source_ps_num*2)
	with allure.step("查看指令保存表"):
		common_store_num=get_t_info.common_store_count()[0]
		allure.attach(f"启动后网元处理指令期望入表{source_ps_num*2},入表的实际数量{common_store_num}")
		print(f"启动后网元处理指令入表的实际数量{common_store_num}")
		pytest.assume(common_store_num>=source_ps_num*2)
	with allure.step("查看ps历史表"):
		ps_table_his_num=get_t_info.ps_table_his_count()[0]
		allure.attach(f"调度处理到ps历史表期望入表{source_ps_num},实际数量为{ps_table_his_num}")
		print(f"ps历史表实际数量为{ps_table_his_num}")
		pytest.assume(ps_table_his_num==source_ps_num)	

if __name__=='__main__':
	save_data_result("result.xlsx")