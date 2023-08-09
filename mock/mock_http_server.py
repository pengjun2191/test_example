from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
import  os,sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from mock.mock_response import send_ch

class Resquest(BaseHTTPRequestHandler): 
    timeout = 5
    server_version = "Apache"   #设置服务器返回的的响应头 
    def set_mock_data_file(self,mock_data_file):
        self.mock_data_file=mock_data_file

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type","text/html")  #设置服务器响应头
        self.send_header("test1","This is test!")     #设置服务器响应头
        self.end_headers()
        buf = send_ch("get",self.mock_data_file)
        self.wfile.write(buf.encode())  #里面需要传入二进制数据，用encode()函数转换为二进制数据   #设置响应body，即前端页面要展示的数据
 
    def do_POST(self):
        path = self.path
        print(path)
        #获取post提交的数据
        datas = self.rfile.read(int(self.headers['content-length']))    #固定格式，获取表单提交的数据
        #datas = urllib.unquote(datas).decode("utf-8", 'ignore')
        print(datas)
        self.send_response(200)
        self.send_header("Content-type","text/html")    #设置post时服务器的响应头
        self.send_header("test","This is post!")
        self.end_headers()
 
        html = send_ch("post",self.mock_data_file)
        self.wfile.write(html.encode())  #提交post数据时，服务器跳转并展示的页面内容

def http_server(server_class=ThreadingHTTPServer, handler_class=Resquest,server_address=('', 8888),mock_data_file="./mock/mock_data/mock_response.xls"):
    try:       
        handler_class.set_mock_data_file(handler_class,mock_data_file)
        httpd = server_class(server_address, handler_class)
        print ('服务已经开启')
        print("listen at: %s:%s" %server_address)
        httpd.serve_forever()
    except Exception as e:
        print ('服务已经结束')  



if __name__ == '__main__':
    from mock_cli import mock_cli
    args=mock_cli()
    http_server(server_address=(args.host, args.port))
   
