# 项目概述
基于python3.8.10开发的测试过程中部分场景常用的脚本代码  
# 项目具体模块说明
mock:实现基础的socket和http服务功能：包含脚本代码和mock服务返回数据  
mail:用于邮件发送，发送邮件给项目相关人员  
common:基础操作module代码，非业务操作基础功能代码模块  
config：测试配置及初始化配置  
pj_function:项目测试业务功能module代码，可以在此部分增加业务测试功能，用于test_case的调用，包括开通进程的启停，历史表数据查询，日志清理等功能  
other_scripts：额外的测试脚本代码，相关第三方调用试验可放置此模块  
tools:对第三方工具模块的操作说明  
report:测试用例结果及用例数据结果目录，从此目录获取测试结果及报告相关内容  
test_case:功能自动化用例,主要书写测试步骤（调用功能）及报告详细展示信息  
test_performance_case:性能测试用例（基于locust实现）  
test_main.py:功能自动化运行开始脚本  
test_performance_main.py:性能自动化运行开始脚本,命令行可选择参数  
test_mock.py:mock服务运行脚本，命令行可选择参数，选择合适的mock协议（当前包括http、soap,socket,mail）进行服务启动，可以用于模拟网元返回（返回数据在xlsx文件中配置）  
pytest.ini:主要用于指定pytest测试范围，匹配测试用例  
requirements.txt:运行依赖通过命令行pipreqs . --encoding=utf8  --force得到,需pip install pipreqs  
注意需要importlib-metadata==4.13.0(已补充在依赖文件中)，高版本舍弃了部分方法，测试用例执行会报错  
