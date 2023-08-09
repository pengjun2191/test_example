import  os,sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from common.KT_op_excel import OpExcel
def send_ch(data,mock_data_file="./mock/mock_data/mock_response.xls",file_sheet="mock_response"):
    if not isinstance(data,str):
        datastr=data.decode()
    else:
        datastr=data
    op_excel=OpExcel(mock_data_file)
    result={}
    for data in op_excel.get_data()[file_sheet]:
        result[data[0]]=data[1]
    return result.get(datastr,"NO macheing return")
if __name__=="__main__":
    print(os.path.realpath("./mock/mock_data/mock_response.xls"))
    print(send_ch("aad",mock_data_file="./mock/mock_data/mock_response.xls",file_sheet="mock_response"))