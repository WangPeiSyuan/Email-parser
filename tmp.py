import MySQLdb
import pandas as pd

## get data from sysmgrdb and preprocess 
HOST="140.115.17.196"
DATABASE="sysmgrdb"
USER="tyrc_ncu"
PASSWORD="Merry34!"

db = MySQLdb.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
cursor = db.cursor()
sql = "select name,email,phone,faculty.did,ip_range,dept.dept from faculty join dept on faculty.did=dept.did where faculty.did<>'cc';" ##排除電算中心人員，因人員太多異動頻繁
# sql = "select * from dept;"
# sql =  "select std_name,email,phone,student.did,ip_range, dept.dept from student join dept on student.did=dept.did ;"
cursor.execute(sql)
print(cursor)
# cnt = 0
for row in cursor:
    if('183' in row[4]):
        print(row)
    # cnt += 1
# print(cnt)