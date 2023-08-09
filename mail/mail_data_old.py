
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.header import Header

class maildata:
    def __init__(self) -> None:
        self.sender = 'from@test.com'
        self.receivers = ['764169118@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
        self.message=None
        #第三方 SMTP 服务
        self.mail_host="localhost"  #设置服务器
        self.mail_user="XXXX"    #用户名
        self.mail_pass="XXXXXX"   #口令 
        self.mail_port=None
        self.from_head="测试"
        self.to_head="开发"
        self.subject=None
    def create_mail_message(self,mail_msg,mail_attach=[],images=[],type='plain',message_code='utf-8',subject='Python SMTP 邮件测试'):
        # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
        if mail_attach!=[]and images==[]:
            self.message=self.set_message_attach(mail_msg,mail_attach,type,message_code)
        elif images!=[]:
            self.message=self.set_message_html_image(mail_msg,mail_attach,images,type,message_code)
        else:
            self.message = MIMEText(mail_msg,type,message_code)
        self.message['From'] = Header(self.from_head, message_code)   # 发送者
        self.message['To'] =  Header(self.to_head, message_code)    # 接收者
        self.subject = subject
        self.message['Subject'] = Header(self.subject, 'utf-8')
    def set_message_attach(self,mail_msg,mail_attach,type,message_code):
        message=MIMEMultipart()
        message.attach(MIMEText(mail_msg,type,message_code))
        for file_name in mail_attach:
            att1 = MIMEText(open(file_name, 'rb').read(), 'base64', 'utf-8')
            att1["Content-Type"] = 'application/octet-stream'
            # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
            att1["Content-Disposition"] = f'attachment; filename={file_name}'
            message.attach(att1)
        return message
    def set_message_html_image(self,mail_msg,images,type,message_code):
        msgRoot = MIMEMultipart()
        msgAlternative =MIMEMultipart()
        msgAlternative.attach(MIMEText(mail_msg,type,message_code))
        msgRoot.attach(msgAlternative)
        i=0
        for image in images:
            mail_msg = f"""<p><img src="cid:image{i}"></p>"""
            msgAlternative.attach(MIMEText(mail_msg, 'html', 'utf-8'))
            fp = open(image, 'rb')
            msgImage = MIMEImage(fp.read())
            fp.close()
            # 定义图片 ID，在 HTML 文本中引用
            msgImage.add_header('Content-ID', f'<image{i}>')
            msgRoot.attach(msgImage)
            i+=1
        return msgRoot
        

