from email.message import EmailMessage
"""
subject: email的主题
body: 主体内容
from_email: 发送者的邮箱地址
to: 接受者的邮箱地址（是一个列表或者元组，发送给一个人或者多个人）
bcc: 使用‘Bcc’头的邮箱地址（一个列表或者元组）
connection: 一个邮件备用实例。如果你想用同一个连接发送多个信息，那么需要使用这个参数。不然的话，发送多条信息给同一个接收人，每次调用send()方法都会重新创建一个新的连接。
attachments: 一个附件的列表。附件可以使email.MIMEBase.MIMBase实例，也可以是元组（文件，目录，多媒体类型文件）。
headers: 一个字典参数，放额外的头部信息。字典关键字是头部的名字，字典的键值是头部的内容。调用者在发送email信息时，要保证头部名和值都是正确的格式。 与之对应的一个形参是extra_headers.
cc: 一个列表或者元组，存放使用"Cc"头的接受者的邮箱地址。
replay_to: 一个列表或者元组， 存放使用"Reply-To"头的接受者的邮箱地址。"""

class maildata:
    def __init__(self) -> None:
        self.sender = 'from@test.com'
        self.receivers = ['764169118@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
        self.cc=None
        self.bcc=None
        self.message=None
        #第三方 SMTP 服务
        self.mail_send_host="localhost"  #设置服务器
        self.mail_send_port=None
        #第三方pop服务
        self.mail_recv_host="localhost"  #设置服务器
        self.mail_recv_port=None       
        #用户信息
        self.mail_user=None    #用户名
        self.mail_pass=None  #口令 
        self.from_head="测试"
        self.to_head="开发"
        self.subject=None

    def create_mail_message(self,mail_msg,mail_attachs=[],subject='Python SMTP 邮件测试'):
        self.message = EmailMessage()
        # 邮件头部
        self.message["From"] =  self.sender 
        self.message["To"] = self.receivers
        self.message["cc"] = self.cc
        self.message["Bcc"] = self.bcc
        # 主题
        self.message["Subject"] = subject
        self.message.set_content(mail_msg)

        if mail_attachs!=[]:
            for mail_attach in mail_attachs:
            # 比如我们附加一个excel文件
                with open(mail_attach, mode="rb") as fp:
                    mail_attach_content = fp.read()
                    self.message.add_attachment(mail_attach_content, maintype="application", filename=mail_attach)
        return self.message