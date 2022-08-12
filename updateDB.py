import MySQLdb
import pandas as pd

## get data from sysmgrdb and preprocess 
db = MySQLdb.connect("localhost", "root", "Tyrcncu0930!", "sysmgrdb", charset="utf8")
cursor = db.cursor()
sql = "select name,email,phone,faculty.did,ip_range from faculty join dept on faculty.did=dept.did where faculty.did<>'cc';"
cursor.execute(sql)

name_list=[]
email_list=[]
phone_list=[]
ip_list=[]
for row in cursor:    
    network = row[4].split(':')
    for seg in network:
        if(seg!=''):
            ip = '140.115.'+seg+'.0/24'
            name_list.append(row[0])
            email_list.append(row[1])
            phone_list.append(row[2])
            # print(ip)
            ip_list.append(ip)

sql = "select std_name,email,phone,student.did,ip_range from student join dept on student.did=dept.did ;"
cursor.execute(sql)
for row in cursor:    
    network = row[4].split(':')
    for seg in network:
        if(seg!=''):
            ip = '140.115.'+seg+'.0/24'
            name_list.append(row[0])
            email_list.append(row[1])
            phone_list.append(row[2])
            # print(ip)
            ip_list.append(ip)
db.close()

df = pd.DataFrame({'name': name_list, 'email': email_list, 'phone': phone_list, 'ip_network': ip_list})
print(df)
df = df.groupby('ip_network').agg(lambda x: ','.join(x[x.notna()]))

## update data in school_net
db = MySQLdb.connect("localhost", "root", "Tyrcncu0930!", "tyrcDB", charset="utf8")
cursor = db.cursor()
count=0
for idx, row in df.iterrows():

    sql = "update school_net set admin_contact='"+row['name']+"', admin_tel='"+row['phone']+"', admin_mail='"+row['email']+"' where ip_network='"+idx+"';"
    cursor.execute(sql)
    db.commit()

    print(cursor.rowcount, " record(s) affected")
db.close()

