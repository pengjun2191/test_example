import pytest
import os
import sys
from mail.mail_data import maildata
from mail.send_mail import smtp_mail_send
from pj_function.get_config import get_config
def getProjectPath():
    #return os.getcwd()
    return os.path.dirname(os.path.realpath(__file__))
def main(*args):

    #测试报告目录
    """
    allure_dir=os.path.join(getProjectPath(),"report","allure_result")
    allure_report=os.path.join(getProjectPath(),"report","allure_report")
    allure_csv=os.path.join(getProjectPath(),"report","allure_csv")
    html_dir=os.path.join(getProjectPath(),"report","html")
    """
    cfg=get_config()
    allure_dir=cfg.test_report_dir["allure_dir"]
    allure_report=cfg.test_report_dir["allure_report"]
    allure_csv=cfg.test_report_dir["allure_csv"]
    html_dir=cfg.test_report_dir["html_dir"]
   
    #执行参数
    param=["-s",
           "-v",
           "--cache-clear",#清空缓存
           f"--html={html_dir}/report.html",#生成Html报告
           f"--alluredir={allure_dir}",#生成allure报告
           "--clean-alluredir"#清理alluredir的json目录
           ]
    try:
        for i in args:
            param.append(i)
    except IndexError as e:
        print (e)
        print ("自定义测试套件不存在")
    #print ("param=",param)
    pytest.main(param)
    os.system(f"allure generate {allure_dir} -o {allure_report} --clean")
    mail_data=maildata()
    mail_data.create_mail_message("'测试完成请登录平台查看结果'",subject="自动化测试已完成请查看结果")
    smtp_mail_send(mail_data)
    #os.system(f"allure open {allure_report}")

if __name__ == '__main__':
    sys.path.append(getProjectPath())
    path_dir=os.path.join(getProjectPath(),"test_case")
    print(path_dir)
    main(path_dir)
    #pytest.main(["-m tableinterface","-sv"])
    