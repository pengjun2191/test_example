import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))



""" 
select * from i_provision_931 ip;
select * from i_provision_his_931_202307 iph ;
select * from i_ps_provision_reset_931 ippr;
select * from ps_provision_931 pp ;
select * from ps_provision_his_931_202307 pph ;
select * from ps_provision_split_931 pps2 ;
select * from ps_split_his_931_202307 psh  ;
select * from ps_async_buffer_his_202105 pabh ;
"""
def query_his(table,*args,**keyword):
    strargs=",".join(args[0])
    sql=f"select {strargs} from {table} "
    if keyword != {}:
        sql=sql+"where"
        for key, value in keyword.items():
            sql=sql+",".join(f"{key}={value}")
    return sql

def delete_table(table):
    sql=f"delete from {table};"
    return sql

def insert_table(table,*args,**keyword):
    bb=[]
    if args is not None:
        strkey=",".join(args[0][0])
        sql=f"insert into {table} ({strkey}) values %s "
        for i in args[0][1:]:
            bb.append(tuple(i))
    elif keyword is not None:
        strkey=",".join(keyword.keys())
        sql=f"insert into {table} ({strkey}) values %s "
        bb.append(tuple(keyword.values()))
    return sql,bb   
        

def update_table_status(table,**keyword):
    bb=[]
    strkey=",".join(keyword.keys())
    sql=f"update {table}  set status=0 FROM (VALUES %s) AS data (id) where ps_id=data.id "
    bb.append(tuple(keyword.values()))
    return sql,bb

if __name__=="__main__":
    pass