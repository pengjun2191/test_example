""" 
修改/etc/sysctl.conf，增加net.ipv4.ip_forward = 1，然后执行sysctl -p马上生效
echo 1 > /proc/sys/net/ipv4/ip_forward
或
sysctl -w net.ipv4.ip_forward=1
恢复
echo 0 > /proc/sys/net/ipv4/ip_forward
#端口映射
iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8081
#源地址变更
iptables -t nat -A POSTROUTING -p tcp -d 4.4.4.4 --dport 8810:8850 -j SNAT --to-source 192.168.2.10
#目的地址变更
iptables -t nat -A PREROUTING -p tcp -d 10.19.30.66 --dport 6655 -j DNAT --to-destination 10.19.30.66:1234
#本地端口变更
iptables -t nat -I OUTPUT -p tcp -o lo --dport 6655 -j REDIRECT --to-ports 1234 
#屏蔽ip
iptables -I INPUT -s 114.232.9.171 -j DROP
#指定开放端口给ip
iptables -I INPUT -s 192.168.1.109 -p tcp --dport 3306 -j ACCEPT
#firewall端口转发配置
# firewall-cmd --list-all
# firewall-cmd --add-forward-port=port=6655:proto=tcp:toport=1234 --zone=public --permanent
# firewall-cmd --permanent --direct --add-rule ipv4 nat OUTPUT 0 -p tcp -o lo --dport 6655 -j REDIRECT --to-ports 1234
# firewall-cmd --add-forward-port=port=6655:proto=tcp:toport=1234:toaddr=10.19.30.66 --zone=public --permanent
# firewall-cmd --reload
# firewall-cmd --list-all
#firewall 端口转发配置删除
# firewall-cmd --list-all
# firewall-cmd --remove-forward-port=port=6655:proto=tcp:toport=1234--zone=public --permanent
# firewall-cmd --permanent --direct --remove-rule ipv4 nat OUTPUT 0 -p tcp -o lo --dport 6655 -j REDIRECT --to-ports 1234
# firewall-cmd --remove-forward-port=port=6655:proto=tcp:toport=1234:toaddr=10.19.30.66 --zone=public --permanent
# firewall-cmd --reload
# firewall-cmd --list-all
"""
#antdb_start='pg_ctl -D /data02/antdb/app/antdb/data start'
#antdb_stop='pg_ctl -D /data02/antdb/app/antdb/data stop'
#antdb_abnormal="""ps -ef |grep postgre|grep -v "grep"|awk '{print $2}'|xargs -r kill -9"""
#antdb_net_reset="iptables -t nat -D OUTPUT -p tcp -o lo --dport 6655 -j REDIRECT --to-ports 1234 "
#antdb_net_break="iptables -t nat -I OUTPUT -p tcp -o lo --dport 6655 -j REDIRECT --to-ports 1234 "

import sys,os
import time
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pj_function.op_antdb_process import op_antdb_process
from pj_function.op_kt_process import op_ktprocess
from pj_function.get_kt_table_info import get_table_info
from test_case.test_common.common_test_step import table_interface_check_histable,save_data_result
import pytest
import allure

get_t_info=get_table_info()
op_kt=op_ktprocess()
op_antdb=op_antdb_process()
@allure.feature("初始化总控进程，检查测试工单入表")
@allure.title("初始化……")
def setup_function():
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
def teardown_function():
	with allure.step("关闭全部进程"):
			op_kt.shutdown_all()
	with allure.step("清理历史表数据"):
			pass
	with allure.step("清理接口表数据"):
			pass


@allure.feature("使用过程中数据库关闭重启")
#@pytest.mark.skip()
def test_db_stop():
    with allure.step("数据库关闭退出"):
        op_antdb.antdb_stop()
    with allure.step("休眠300s"):
        time.sleep(300) 
    with allure.step("检查日志"):
        pass
    with allure.step("数据库启动"):
        op_antdb.antdb_start()
    with allure.step("休眠300s"):
        time.sleep(300) 

    table_interface_check_histable(i_table_count_num)
    save_data_result()

@allure.feature("使用过程中数据库异常关闭并重启")
#@pytest.mark.skip()
def test_db_abnormal():
    with allure.step("数据库异常关闭"):
        op_antdb.antdb_abnormal()
    with allure.step("休眠120s"):
        time.sleep(120) 
    with allure.step("检查日志"):
        pass
    with allure.step("数据库启动"):
        op_antdb.antdb_start()

    table_interface_check_histable(i_table_count_num)
    save_data_result()
    
@allure.feature("使用过程中网络端口异常断连——使用iptables方式实现端口转发导致异常并恢复")
#@pytest.mark.skip()
def test_iptables_netbreak():
    with allure.step("设置端口转发_异常"):
        op_antdb.antdb_net_break()
        op_antdb.antdb_iptables_break()
    with allure.step("休眠300"):
         time.sleep(300)
    with allure.step("检查日志"):
        pass
    with allure.step("恢复端口转发"):
        net_reset()

    table_interface_check_histable(i_table_count_num)
    save_data_result()

#数据库端口转发删除
def net_reset():
    op_antdb.antdb_net_reset()
    op_antdb.antdb_iptables_reset()

   
@allure.feature("使用过程中网络端口异常断连——使用firewall方式实现端口转发导致异常并恢复")
#@pytest.mark.skip()
def test_firewall_netbreak():
    with allure.step("设置端口转发_异常"):
        op_antdb.antdb_firewall_break()
    with allure.step("数据库重启"):
         op_antdb.antdb_stop()
         time.sleep(600)
         op_antdb.antdb_start()
    with allure.step("休眠600"):
         time.sleep(600)
    with allure.step("检查日志"):
        pass
    with allure.step("恢复端口转发"):
        op_antdb.antdb_firewall_reset()

    table_interface_check_histable(i_table_count_num)
    save_data_result()
if __name__=='__main__':
    pytest.main(["./test_db_exception.py","-sv"])