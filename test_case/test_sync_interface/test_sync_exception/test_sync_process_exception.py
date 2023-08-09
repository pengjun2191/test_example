import sys,os
import time
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pj_function.get_kt_process_in_db import get_process_info
from pj_function.op_kt_process import op_ktprocess
from pj_function.get_kt_table_info import get_table_info
from pj_function.get_kt_RT_interface_data import kt_rt_data
from test_case.test_common.common_test_step import sync_interface_check_histable,save_data_result
import pytest
import allure

get_t_info=get_table_info()
op_kt=op_ktprocess()
get_process=get_process_info()
@allure.feature("初始化总控进程，检查测试工单入表")
@allure.title("初始化……")
def setup_function():
    with allure.step("检查测试工单入表"):
        global rt_data
        rt_data=kt_rt_data()
        if rt_data!=10000:
            allure.attach(f"i表实际数量{rt_data}")
            print (f"i表实际数量{rt_data}")
    with allure.step("启动全部进程"):
        op_kt.start_all()


@allure.feature("清理环境，关闭进程")
@allure.title("清理开始……")
def teardown_function():
	with allure.step("关闭全部进程"):
			op_kt.shutdown_all()
	with allure.step("清理历史表数据"):
			pass
	with allure.step("清理接口表数据"):
			pass

@allure.feature("如果使用webservice，则需要执行此实时拆分全部异常用例")
#@pytest.mark.skip()
def test_killall_split():
    with allure.step("拆分异常关闭"):
        op_kt.kill_excption_spliter()
    with allure.step("休眠120s"):
        time.sleep(120) 
    with allure.step("检查日志"):
        pass
    with allure.step("拆分启动"):
        for split_name in get_process.get_RT_spliter_name():
            op_kt.start_split(split_name[0])
    sync_interface_check_histable(rt_data)
    save_data_result()
    
@allure.feature("使用过程中全部网元异常")
#@pytest.mark.skip()
def test_killall_busicomm():
    with allure.step("使用过程中网元异常"):
        op_kt.kill_excption_busicomm()
    with allure.step("休眠120"):
        time.sleep(120) 
    with allure.step("检查日志"):
        pass
    with allure.step("网元恢复"):
        for busicomm_name in get_process.get_busicomm_name():
            op_kt.start_busicomm(busicomm_name[0])
    sync_interface_check_histable(rt_data)
    save_data_result()
   
@allure.feature("如果使用webservice，则需要执行此实时拆分部分异常用例")
#@pytest.mark.skip()
def test_killone_split():
    split_name_list=get_process.get_RT_spliter_name()
    with allure.step("拆分异常关闭"):
        op_kt.kill_excption_process(split_name_list[0][0])
    with allure.step("休眠120s"):
        time.sleep(120) 
    with allure.step("检查日志"):
        pass
    with allure.step("拆分启动"):
        op_kt.start_split(split_name_list[0][0])
    sync_interface_check_histable(rt_data)
    save_data_result()

    
@allure.feature("使用过程中部分网元异常")
#@pytest.mark.skip()
def test_killone_busicomm():
    busicomm_name_list=get_process.get_busicomm_name()
    with allure.step("使用过程中网元异常"):
        op_kt.kill_excption_process(busicomm_name_list[0][0])
    with allure.step("休眠120"):
        time.sleep(120) 
    with allure.step("检查日志"):
        pass
    with allure.step("网元恢复"):
        op_kt.start_busicomm(busicomm_name_list[0][0])
    sync_interface_check_histable(rt_data)
    save_data_result()

if __name__=='__main__':
    pytest.main(["./test_teble_process_exception.py","-sv"])