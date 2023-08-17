import  os,sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from common.KT_op_webservice import  op_webservice
from pj_function.get_config import cfg_singleton as cfg
from common.KT_op_socket import op_socket
import struct

class op_ktsync:
    def __init__(self) -> None:
        self.webserviceurl=cfg.webserviceurl["webservice"]
        
    def webservice_qry_sendProv(self,timeOut,billId,doneCode,actionId,psServiceType,regionCode,strParam):
        """webservice的查询接口"""
        client = op_webservice(self.webserviceurl).create_client()
        #qry_sendProv(String timeOut, String billId, String doneCode, String actionId, String psServiceType,String regionCode, String strParam)
        result = client.service.qry_sendProv(timeOut,billId,doneCode,actionId,psServiceType,regionCode,strParam)
        # 打印结果
        return result
    def send_split_socket(self):
        pass
    def send_busicomm_socket(self,client_address,bufsiz=4096,**keywords):  
        s=op_socket()
        s.sc_ip=client_address[0]
        s.sc_port=client_address[1]
        s.sc_bufsize=bufsiz
        s.connect()
        print('connect success')      
        ps_net_code=keywords["ps_net_code"]
        ps_id=keywords["ps_id"]
        action_id=keywords["action_id"]
        service_type=keywords["service_type"]
        switch_id=keywords["switch_id"]
        service=keywords["service"]
        data=keywords["ps_param"]
        status=0 
        try:
            data_all=struct.pack('>4sI20s16s10s32s32s128sI%ds'%(len(data)),'AISC',len(data),ps_net_code,ps_id,action_id,service_type,switch_id,service,status,data)
            # print repr(data_all)
            # print (struct.unpack('>4sI20s16s10s32s32s128sI%ds'%(len(data)),data_all))
            s.sc_send(data_all)
            print('send prov success')
            data_recv=s.sc_recv()
            print (data_recv)
        except Exception as err:
            print (err)
        else:
            s.close()

if __name__=="__main__":
    url="http://localhost:7777?wsdl"
    # 创建客户端并解析WSDL文件测试连接mock的soapserver
    client = op_webservice(url).create_client()
    # 调用Webservices接口
    #qry_sendProv(String timeOut, String billId, String doneCode, String actionId, String psServiceType,String regionCode, String strParam)
    result = client.service.test('aa')
    # 打印结果
    print(result)