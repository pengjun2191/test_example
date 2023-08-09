import pytest,allure,time
from pj_function.get_kt_http_interface_data import target_queue
from pj_function.op_kt_http_interface import send_http_thread
from pj_function.op_kt_process import op_ktprocess
from test_case.test_common.common_test_step import save_data_result


op_kt=op_ktprocess()
@allure.feature("初始化进程")
@allure.title("初始化……")
def setup_function():
    global data_queue
    with allure.step("生成数据发送队列"):
        data_queue=target_queue()
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


@allure.feature("测试http服务接收工单功能")
#@pytest.mark.skip()
def test_killall_split():
    with allure.step("多线程发送数据"):
        send_http_thread(data_queue)
    with allure.step("休眠120s"):
        time.sleep(120) 
    with allure.step("检查日志"):
        pass
    save_data_result()
