import allure
import pytest
import time
from pj_function.op_kt_process import op_ktprocess
from pj_function.get_kt_process_in_db import get_process_info
from pj_function.get_kt_table_info import get_table_info
from test_case.test_common.common_test_step import save_data_result

get_t_info=get_table_info()
op_kt=op_ktprocess()
get_process=get_process_info()
'''Blocker级别:阻塞,Critical级别:严重,Normal级别:正常,Minor级别:不太重要,Trivial级别:不重要'''

@allure.severity(allure.severity_level.BLOCKER)
@allure.feature("实时接口测试")
@pytest.mark.sync
class TestSyncInterface():

    @allure.story("初始化总控进程，检查测试工单入表")
    @allure.title("初始化……")
    def setup_class(self):
        with allure.step("启动总控"):
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
            op_kt.shutdown_all
            save_data_result("TestSyncInterface.xlsx")
        with allure.step("清理历史表数据"):
            pass
        with allure.step("清理接口表数据"):
            pass
                
    @allure.story("实时拆分测试")
    @allure.title("实时拆分测试")
    @pytest.mark.syncsplit
    def test_syncsplit(self):
        with allure.step("启动实时拆分"):
            for spliter_name in get_process.get_RT_spliter_name():
                op_kt.start_split(spliter_name[0])
        with allure.step("查看日志"):
            pass
        with allure.step("发送工单"):
            pass
        time.sleep(60)
        with allure.step("查看拆分表"):
            pytest.assume(get_t_info.split_table_count==10000)
        with allure.step("启动网元进程"):
            for busicom_name in get_process.get_busicomm_name():
                op_kt.start_busicomm(busicom_name[0])
        with allure.step("休眠900s等待恢复连接，进程处理"):
            time.sleep(900) 
        with allure.step("检查split历史表"): 
            pytest.assume(get_t_info.split_table_his_count()[0]==20000)
        with allure.step("检查ps历史表"): 
            pytest.assume(get_t_info.ps_table_his_count()[0]==10000)
    

if __name__ == '__main__':
	pytest.main(["./test_sync_interface.py","-sv"])