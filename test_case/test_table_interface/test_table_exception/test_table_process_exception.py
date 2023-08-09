import sys,os
import time
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pj_function.get_kt_process_in_db import get_process_info
from pj_function.op_kt_process import op_ktprocess
from pj_function.get_kt_table_info import get_table_info
from test_case.test_common.common_test_step import table_interface_check_histable,save_data_result
import pytest
import allure

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



@allure.feature("使用过程中调度异常")
#@pytest.mark.skip()
def test_kill_dispatch():
    with allure.step("调度异常关闭退出"):
        op_kt.kill_excption_dispatcher()
    with allure.step("休眠60s"):
        time.sleep(60) 
    with allure.step("检查日志"):
        pass
    with allure.step("调度启动"):
        dispatch_names=get_process.get_dispatch_name()
        for dispatch_name in dispatch_names:
            op_kt.start_dispatch(dispatch_name[0])
        allure.attach(f"启动的调度进程{dispatch_names}")	

    with allure.step("查看日志"):
        pass
    table_interface_check_histable(i_table_count_num)
    save_data_result()

@allure.feature("使用过程中全部拆分异常")
#@pytest.mark.skip()
def test_killall_split():
    with allure.step("拆分异常关闭"):
        op_kt.kill_excption_spliter()
    with allure.step("休眠60s"):
        time.sleep(60) 
    with allure.step("检查日志"):
        pass
    with allure.step("拆分启动"):
        split_names=get_process.get_normal_spliter_name()
        for split_name in split_names:
            op_kt.start_split(split_name[0])
        allure.attach(f"启动的调度进程{split_names}")

    with allure.step("查看日志"):
        pass
    table_interface_check_histable(i_table_count_num)
    save_data_result()
    
@allure.feature("使用过程中全部网元异常")
#@pytest.mark.skip()
def test_killall_busicomm():
    with allure.step("使用过程中网元异常"):
        op_kt.kill_excption_busicomm()
    with allure.step("休眠60"):
        time.sleep(60) 
    with allure.step("检查日志"):
        pass
    with allure.step("网元恢复"):
        busicomm_names=get_process.get_busicomm_name()
        for busicomm_name in busicomm_names:
            op_kt.start_busicomm(busicomm_name[0])
        allure.attach(f"启动的网元进程是{busicomm_names}")

    with allure.step("查看日志"):
        pass
    table_interface_check_histable(i_table_count_num)
    save_data_result()
   
@allure.feature("使用过程中部分拆分异常")
#@pytest.mark.skip()
def test_killone_split():
    split_name_list=get_process.get_normal_spliter_name()
    with allure.step("拆分异常关闭"):
        op_kt.kill_excption_process(split_name_list[0][0])
        allure.attach(f"异常关闭的拆分进程是{split_name_list[0][0]}")
    with allure.step("休眠60s"):
        time.sleep(60) 
    with allure.step("检查日志"):
        pass
    with allure.step("拆分启动"):
        op_kt.start_split(split_name_list[0][0])
        allure.attach(f"重启的拆分进程是{split_name_list[0][0]}")

    with allure.step("查看日志"):
        pass
    table_interface_check_histable(i_table_count_num)
    save_data_result()
    
@allure.feature("使用过程中部分网元异常")
#@pytest.mark.skip()
def test_killone_busicomm():
    busicomm_name_list=get_process.get_busicomm_name()
    with allure.step("使用过程中网元异常"):
        op_kt.kill_excption_process(busicomm_name_list[0][0])
        allure.attach(f"异常关闭的网元进程是{busicomm_name_list[0][0]}")
    with allure.step("休眠60"):
        time.sleep(60) 
    with allure.step("检查日志"):
        pass
    with allure.step("网元恢复"):
        op_kt.start_busicomm(busicomm_name_list[0][0])
        allure.attach(f"重启的网元进程是{busicomm_name_list[0][0]}")

    with allure.step("查看日志"):
        pass
    table_interface_check_histable(i_table_count_num)
    save_data_result()
if __name__=='__main__':
    pytest.main(["./test_teble_process_exception.py","-sv"])