import time
import pytest
import allure
from pj_function.op_kt_process import op_ktprocess
from pj_function.get_kt_process_in_db import get_process_info
from pj_function.get_kt_table_info import get_table_info
from test_case.test_common.common_test_step import table_interface_check_histable,save_data_result

get_t_info=get_table_info()
op_kt=op_ktprocess()
get_process=get_process_info()

@allure.feature("初始化总控进程，检查测试工单入表")
@allure.title("初始化……")
def setup_function(self):
	with allure.step("检查测试工单入表"):
		global i_table_count_num
		i_table_count_num=get_t_info.i_table_count()[0]
		if i_table_count_num!=10000:
			allure.attach(f"i表实际数量{i_table_count_num}")
			print (f"i表实际数量{i_table_count_num}")
	with allure.step("启动全部进程"):
		op_kt.start_all()

@allure.feature("清理环境，关闭进程")
@allure.title("清理开始……")
def teardown_function(self):
	with allure.step("关闭全部进程"):
			op_kt.shutdown_all()
	with allure.step("清理历史表数据"):
			pass
	with allure.step("清理接口表数据"):
			pass
	

@allure.title("调度重启处理案例")
@allure.feature("调度重启可重发处理工单")
@pytest.mark.run(order=6)
#@pytest.mark.skip
def test_rerun_dispatch():
	dispatch_names=get_process.get_dispatch_name()
	with allure.step("关闭调度进程"):
		if get_t_info.ps_table_count_status_running()[0]>0 :
			for shutdown_dispach_name in dispatch_names:
				op_kt.shutdown_dispatch(shutdown_dispach_name[0])
				while op_kt.get_app_start_num_by_process_name(shutdown_dispach_name[0]) >0:
					time.sleep(10)	
			allure.attach(f"关闭的调度进程{shutdown_dispach_name}")	
	with allure.step("休眠60s等待恢复启动"):
		time.sleep(60) 
	with allure.step("启动调度进程"):
		for dispatch_name in dispatch_names:
			op_kt.start_dispatch(dispatch_name[0])
		allure.attach(f"启动的调度进程{dispatch_names}")

	with allure.step("查看日志"):
		pass
	table_interface_check_histable(i_table_count_num)
	save_data_result()

@allure.title("拆分重启处理案例")
@allure.feature("拆分重启继续处理")
@pytest.mark.run(order=7)
#@pytest.mark.skip
def test_rerun_split():
	split_names=get_process.get_normal_spliter_name()
	with allure.step("关闭拆分进程"):
		if get_t_info.split_table_count_status_running()[0]>0 :
			for shutdown_split_name in split_names:
				op_kt.shutdown_split(shutdown_split_name[0])
				while op_kt.get_app_start_num_by_process_name(shutdown_split_name[0]) >0:
					time.sleep(10)	
		allure.attach(f"关闭的拆分进程{split_names}")	
	with allure.step("休眠60s等待恢复启动"):
		time.sleep(60)
	with allure.step("启动拆分进程"):
		for split_name in split_names:
			op_kt.start_split(split_name[0])
		allure.attach(f"启动的拆分进程{split_names}")
	with allure.step("休眠960等待恢复连接，进程处理"):
		time.sleep(960) 
	with allure.step("查看日志"):
		pass
	table_interface_check_histable(i_table_count_num)
	save_data_result()
	

@allure.title("网元重启处理案例")
@allure.feature("网元重启继续处理")
@pytest.mark.run(order=8)
#@pytest.mark.skip
def test_rerun_busicomm():
	"""网元流程休眠20ms"""
	time_num=0
	busicomm_names=get_process.get_busicomm_name()
	with allure.step("关闭网元进程"):
		if get_t_info.split_table_count_status_running()[0]>0 :
			for shutdown_busicomm_name in busicomm_names:
				op_kt.shutdown_busicomm(shutdown_busicomm_name[0])
		while op_kt.get_busicomm_start_num()>0:
			time.sleep(10)	
			time_num+=10
			if time_num%100==0:
				for shutdown_busicomm_name in busicomm_names:
					op_kt.shutdown_busicomm(shutdown_busicomm_name[0])
		allure.attach(f"关闭的网元进程{busicomm_names}")	
	with allure.step("休眠60s等待恢复启动"):
		time.sleep(60)
	with allure.step("启动网元进程"):
		for busicomm_name in busicomm_names:
			op_kt.start_busicomm(busicomm_name[0])
		allure.attach(f"启动的拆分进程{busicomm_names}")

	with allure.step("查看日志"):
		pass
	table_interface_check_histable(i_table_count_num)
	save_data_result()


if __name__ == '__main__':
	pytest.main(["./test_table_interface.py","-sv"])
