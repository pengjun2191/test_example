import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from common.KT_op_excel import OpExcel
from pj_function.get_config import get_config
from pj_function.get_kt_table_info import get_table_info
import json,datetime
from queue import Queue
from copy import deepcopy,copy

"""生成模拟CRM发送的http工单json数据队列"""
get_t_info=get_table_info()
cfg_db=get_config()

table_values=  {"ps_id":None,
                "busi_code":None,
                "extern_id":None,
                "done_code":None,
                "ps_type":None,
                "prio_level":None,
                "dead_line":None,
                "sort_id":None,
                "ps_service_type":None,
                "bill_id":None,
                "sub_bill_id":None,
                "plan_id":None,
                "sub_valid_date":None,
                "upp_create_date":None,
                "create_date":None,
                "start_date":None,
                "end_date":None,
                "ret_date":None,
                "status_upd_date":None,
                "mon_flag":None,
                "action_id":None,
                "old_ps_param":None,
                "ps_param":None,
                "target_param":None,
                "ps_status":None,
                "fail_num":None,
                "fail_reason":None,
                "fail_code":None,
                "hand_id":None,
                "hand_op_id":None,
                "hand_notes":None,
                "ret_op_id":None,
                "ret_notes":None,
                "op_id":None}


def check_i_table(table):
    TABLE=table.split("_")
    if TABLE[0]=="i" and TABLE[1]=="provision":
        TABLE_REGIN_CODE=table.split("_")[2]
        src_value={"TABLE_REGIN_CODE":TABLE_REGIN_CODE,"ORDERS":None}
        return src_value
    else:
        return "table is not i_provision_xxx"
    

def src_queue(values):
    bb=Queue()
    for i in range(1,len(values)):
        for j in range(0,len(values[0])):
            if isinstance(values[i][j],datetime.datetime):
                table_values[values[0][j]]=values[i][j].strftime('%Y%m%d%H%M%S')
            else:
                table_values[values[0][j]]=values[i][j]
        a=copy(table_values)
        bb.put(a)
    return bb


def change_json(src_value,ps_q:Queue):
    bb=[]
    try:
        for i in range(0,10):
            a=ps_q.get_nowait()
            bb.append(a)
    except:
        pass
    finally:
        if bb !=[]:
            src_value["ORDERS"]=bb
            return json.dumps(src_value)
        
def target_queue():
    t_queue=Queue()
    opExcel=OpExcel(cfg_db.TestData["file"])
    table_dict=opExcel.get_data()
    for key,values in table_dict.items():
        ps_q=src_queue(values)
        while not ps_q.empty():
            t_queue.put(change_json(check_i_table(key),ps_q))
    return t_queue

def parse_result(result):
    result_dict=json.loads(result)
    return result_dict



if __name__=="__main__":
    target_queue()


