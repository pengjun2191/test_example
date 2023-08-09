import psycopg2
from psycopg2 import extras
import cx_Oracle 


dbip_oracle="10.10.10.124"
dbport_oracle="1521"
dbname_oracle="oel1247"
dbuser_oracle="lnkt4"
dbpwd_oracle="lnkt4"

dbuser_antdb = "user1"
dbip_antdb  = "10.19.30.66"
dbname_antdb  = "testdb3"
dbport_antdb  = "6655"
dbpwd_antdb  = "456@789@321"

#antdb
sqls_delete_antdb="delete from ps_test_phone ptp;"
sqls_query_antdb="select * from ps_test_phone ptp"
sqls_antdb="insert into ps_test_phone (bill_id,imsi) values %s"
values_antdb=[(12345678901,1987654322221212),(21234568901,2987654322221212)]
conn_antdb=psycopg2.connect(database="testdb3",user="user1",password="456@789@321",host="10.19.30.66",port="6655")
cursor_antdb=conn_antdb.cursor()
cursor_antdb.execute(sqls_delete_antdb)
extras.execute_values(cursor_antdb,sqls_antdb,values_antdb)
conn_antdb.commit()
cursor_antdb.execute(sqls_query_antdb)
results_antdb=cursor_antdb.fetchall()
print(results_antdb)
cursor_antdb.close()
conn_antdb.close()



#oracle
sqls_delete_oracle="delete from ps_test_phone ptp"
sqls_query_oracle="select * from ps_test_phone ptp"
sqls_oracle="insert into ps_test_phone (bill_id,imsi) values (:1,:2)"
values_oracle=[(12345678901,1987654322221212),(21234568901,2987654322221212)]
dsn =cx_Oracle.makedsn(dbip_oracle,dbport_oracle,dbname_oracle)
conn_oracle=cx_Oracle.connect(dbuser_oracle,dbpwd_oracle,dsn)
cursor_oracle =conn_oracle.cursor()
cursor_oracle.execute(sqls_delete_oracle)
cursor_oracle.executemany(sqls_oracle,values_oracle)
conn_oracle.commit()
cursor_oracle.execute(sqls_query_antdb)
results_oracle=cursor_oracle.fetchall()
print(results_oracle)
cursor_oracle.close()
conn_oracle.close()


