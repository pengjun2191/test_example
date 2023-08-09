#!/usr/bin/python
# -*- coding: UTF-8 -*-
 
import smtplib
from mail_data import maildata 

def smtp_mail_send(emaildata:maildata):
    try:
        smtpObj = smtplib.SMTP(emaildata.mail_send_host,emaildata.mail_send_port)
        if emaildata.mail_host!="localhost":
            smtpObj.login(emaildata.mail_user,emaildata.mail_pass)
        smtpObj.sendmail(emaildata.sender, emaildata.receivers, emaildata.message.as_string())
        print ("邮件发送成功")
    except smtplib.SMTPException as e:
        print (e)
        print ("邮件发送失败")

if __name__=="__main__":
    mail_data=maildata()
    mail_data.create_mail_message("'Python 邮件发送测试...'","")
    smtp_mail_send(mail_data)