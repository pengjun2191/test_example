from email.parser import Parser
import poplib
from mail_data import maildata 

def pop3_mail_get(emaildata:maildata):
    pop_conn = poplib.POP3(emaildata.mail_recv_host,emaildata.mail_recv_port)
    pop_conn.user(emaildata.mail_user)
    pop_conn.pass_(emaildata.mail_pass)
    # 获取所有信件的数量和占用空间
    num_msgs, mailbox_size = pop_conn.stat()
    print(num_msgs,mailbox_size)

    # 获取最近一封信件的编号和占用空间
    print(str(pop_conn.list()[1][-1],encoding='utf-8').split(" "))
    last_email_num, last_email_size = str(pop_conn.list()[1][-1],encoding='utf-8').split(" ")
    print(f"mail size:{last_email_size}")

    # 获取最近一封信件的内容（bytes 类型）
    response, lines, bytes = pop_conn.retr(last_email_num)
    email_content = b'\n'.join(lines).decode('utf-8')
    pop_conn.quit()
    print (f"{response} size: {bytes}")
    return email_content

def mail_Parser(mail_content):
    headers  = Parser().parsestr(mail_content)   #经过parsestr处理过后生成一个字典
    print  ('Cc: %s'  %  headers[ 'Cc' ])
    print  ('To: %s' %  headers[ 'to' ])
    print  ('From: %s'  %  headers[ 'from' ])
    print  ('Subject: %s'  %  headers[ 'subject' ])

if __name__=="__main__":
    mail_data=maildata()
    mail_data.mail_recv_host=""
    mail_data.mail_recv_port=110
    mail_data.mail_user=""
    mail_data.mail_pass=""
    mail_Parser(pop3_mail_get(mail_data))