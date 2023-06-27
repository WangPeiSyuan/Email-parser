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
cursor.execute(sql)

name_list=[]
email_list=[]
phone_list=[]
ip_list=[]
office_list=[]
for row in cursor:    
    network = row[4].split(':')
    for seg in network:
        if(seg!=''):
            if('/' in seg):
                ip = '140.115.'+seg
            else:
                ip = '140.115.'+seg+'.0/24'
            name_list.append(row[0])
            email_list.append(row[1])
            phone_list.append(row[2])
            office_list.append('中央大學'+row[5])
            ip_list.append(ip)

sql =  "select std_name,email,phone,student.did,ip_range,dept.dept from student join dept on student.did=dept.did ;"
cursor.execute(sql)
for row in cursor:    
    network = row[4].split(':')
    for seg in network:
        if(seg!=''):
            if(seg!=''):
                if('/' in seg):
                    ip = '140.115.'+seg
                else:
                    ip = '140.115.'+seg+'.0/24'
            name_list.append(row[0])
            email_list.append(row[1])
            phone_list.append(row[2])
            office_list.append('中央大學'+row[5])
            ip_list.append(ip)
db.close()

df = pd.DataFrame({'name': name_list, 'email': email_list, 'phone': phone_list, 'ip_network': ip_list, 'office':office_list})
# print(df)
df = df.groupby(['ip_network', 'office']).agg(lambda x: ','.join(x[x.notna()]))
# print(df)
## update data in school_net
db = MySQLdb.connect("localhost", "root", "Tyrcncu0930!", "tyrcDB", charset="utf8")
cursor = db.cursor()
update_cnt = 0
insert_cnt = 0
sql_list = []
for idx, row in df.iterrows():
    sql = "select ip_network from school_net where ip_network='"+idx[0]+"';"
    cursor.execute(sql)
    if(cursor.rowcount!=0):
        sql = "update school_net set admin_contact='"+row['name']+"', admin_tel='"+row['phone']+"', admin_mail='"+row['email']+"', network_name='"+idx[1]+"' where ip_network='"+idx[0]+"';"
        update_cnt += 1
    else:
        sql = "insert into school_net (admin_contact, admin_tel, admin_mail, ip_network, network_name, mail_notify, line_notify) values ('"+row['name']+"', '"+row['phone']+"','"+row['email']+"','"+idx[0]+"','"+idx[1]+"', '1', '0');"
        insert_cnt += 1
    sql_list.append(sql)

    cursor.execute(sql)
    db.commit()
print("共更新{}筆資料, 新增{}筆資料".format(update_cnt, insert_cnt))
for sql in sql_list:
    print(sql)
db.close()
print("Update successfully!")

