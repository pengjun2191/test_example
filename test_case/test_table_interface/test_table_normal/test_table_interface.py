import time
import pytest
import allure
from pj_function.op_kt_process import op_ktprocess
from pj_function.get_kt_process_in_db import get_process_info
from pj_function.get_kt_table_info import get_table_info
from test_case.test_common.common_test_step import save_data_result

get_t_info=get_table_info()
op_kt=op_ktprocess()
get_process=get_process_info()
def setup_module():
	pass

@allure.severity(allure.severity_level.BLOCKER)
@allure.feature("表接口测试")
@pytest.mark.tableinterface
class TestTableInterface():
	"""正常的测试案例一个个进程启停，总控——版本——调度（并检查接口表）——拆分（并检查拆分表）——网元（并检查指令保存表，需要开启指令保存）"""
	@allure.story("初始化总控进程，检查测试工单入表")
	@allure.title("初始化……")
	def setup_class(self):
		with allure.step("检查测试工单入表"):
			global i_table_count_num
			i_table_count_num=get_t_info.i_table_count()[0]
			if i_table_count_num!=10000:
				allure.attach(f"i表实际数量{i_table_count_num}")
				print (f"i表实际数量{i_table_count_num}")
		with allure.step("启动总控+版本进程"):
			if op_kt.get_app_start_num()==0:
				op_kt.start_appControl()
				for version_name in get_process.get_cfgversion_name():
					op_kt.start_cfgversion(version_name[0])
			elif op_kt.get_app_start_num()>0:
				op_kt.shutdown_all()
				op_kt.start_appControl()
				for version_name in get_process.get_cfgversion_name():
					op_kt.start_cfgversion(version_name[0])

	@allure.story("清理环境，关闭进程")
	@allure.title("清理开始……")
	def teardown_class(self):
		with allure.step("关闭全部进程"):
				op_kt.shutdown_all()
		with allure.step("清理历史表数据"):
				pass
		with allure.step("清理接口表数据"):
				pass
		
	
	@allure.title("第一步:调度入表工单处理")
	@allure.story("调度入表工单处理")
	@pytest.mark.run(order=1)
	def test_dispatch(self):
		with allure.step("启动调度进程"):
			dispatch_names=get_process.get_dispatch_name()
			for dispatch_name in dispatch_names:
				op_kt.start_dispatch(dispatch_name[0])
			allure.attach(f"启动的调度进程{dispatch_names}")
		with allure.step("休眠300s等待恢复连接，进程处理"):
			time.sleep(300) 
		with allure.step("查看日志"):
			pass
		with allure.step("查看i历史表"):
			i_table_his_num=get_t_info.i_table_his_count()[0]
			allure.attach(f"i历史表实际数量为{i_table_his_num}")
			pytest.assume(i_table_his_num==i_table_count_num)
		with allure.step("查看ps表"):
			ps_table_num=get_t_info.ps_table_count()[0]
			allure.attach(f"休眠300秒调度实际处理到ps表数量为{ps_table_num}")
			pytest.assume(ps_table_num==i_table_count_num)
		save_data_result()

	@allure.title("第五步:调度回执处理")
	@allure.story("调度回执处理")
	@pytest.mark.run(order=5)
	def test_dispatch_reset(self):
		with allure.step("查看ps历史表"):
			ps_table_his_num=get_t_info.ps_table_his_count()[0]
			allure.attach(f"调度回执处理进ps历史表的实际数量{ps_table_his_num}")
			pytest.assume(ps_table_his_num==i_table_count_num)
		with allure.step("查看reset表"):
			reset_table_num=get_t_info.reset_table_count()[0]
			allure.attach(f"调度回执处理到reset表的实际数量{reset_table_num}")
			pytest.assume(reset_table_num==i_table_count_num)
		save_data_result()

	@allure.title("第二步:拆分连接处理")
	@allure.story("拆分连接处理")
	@pytest.mark.run(order=2)
	def test_split(self):
		with allure.step("启动拆分进程"):
			split_names=get_process.get_normal_spliter_name()
			for split_name in split_names:
				op_kt.start_split(split_name[0])
			allure.attach(f"启动的拆分进程{split_names}")
		with allure.step("休眠600等待恢复连接，进程处理"):
			time.sleep(600) 
		with allure.step("查看日志"):
			pass
		with allure.step("查看split表"):
			split_table_num=get_t_info.split_table_count()[0]
			allure.attach(f"启动600秒后拆分处理到split表的实际数量{split_table_num}")
			pytest.assume(split_table_num==i_table_count_num*2)
		save_data_result()
		
	@allure.title("第四步:拆分处理网元回执")
	@allure.story("拆分处理网元回执")
	@pytest.mark.run(order=4)
	def test_split_recv(self):
		with allure.step("查看split历史表"):
			split_table_his_num=get_t_info.split_table_his_count()[0]
			allure.attach(f"拆分回执处理到split历史表的实际数量{split_table_his_num}")
			pytest.assume(split_table_his_num==i_table_count_num*2)
		save_data_result()

	@allure.title("第三步:网元连接")
	@allure.story("网元连接")
	@pytest.mark.run(order=3)
	def test_busicomm(self):
		"""网元流程休眠20ms"""
		with allure.step("启动网元进程"):
			busicomm_names=get_process.get_busicomm_name()
			for busicomm_name in busicomm_names:
				op_kt.start_busicomm(busicomm_name[0])
			allure.attach(f"启动的拆分进程{busicomm_names}")
		with allure.step("休眠600等待恢复连接，进程处理"):
			time.sleep(1200) 		
		with allure.step("查看日志"):
			pass
		with allure.step("查看指令保存表"):
			common_store_num=get_t_info.common_store_count()[0]
			allure.attach(f"启动600秒后网元处理指令入表的实际数量{common_store_num}")
			pytest.assume(common_store_num==i_table_count_num*2)
		save_data_result()

if __name__ == '__main__':
	pytest.main(["./test_table_interface.py","-sv"])
