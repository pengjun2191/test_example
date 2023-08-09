from spyne import Application,rpc,ServiceBase, String
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server
import  os,sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from mock.mock_response import send_ch

class TestWebService(ServiceBase):

    @rpc(String, _returns=String)
    def test(self,msg):
        try:
            return send_ch(msg)
        except Exception:
            return "错误!"
        
def soap_server(server_address,mock_data_file):
    try:
        soap_app = Application([TestWebService], 'http://webservice.tfc.tmri.com',
                                in_protocol=Soap11(),
                                out_protocol=Soap11())
        wsgi_app = WsgiApplication(soap_app)
        server = make_server(server_address[0], server_address[1], wsgi_app)
        print ('服务已经开启')
        print("http://%s:%s/?wsdl"%server_address)
        server.serve_forever()
    except ImportError:
        print ('服务已经结束')   
       
if __name__=='__main__':  #发布服务    
    from mock_cli import mock_cli
    args=mock_cli()  
    soap_server((args.host,args.port),args.mock_data_file)