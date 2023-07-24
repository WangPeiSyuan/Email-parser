import MySQLdb
import pandas as pd
import configparser

## get data from sysmgrdb and preprocess 
data = configparser.ConfigParser()
data.read('config.ini')
host = data['sysmgrDB']['HOST']
user = data['sysmgrDB']['USER']
passwd = data['sysmgrDB']['PASSWORD']
database = data['sysmgrDB']['DB']
db = MySQLdb.connect(host, user, passwd, database)
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
            office_list.append('中大'+row[5])
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
            office_list.append('中大'+row[5])
            ip_list.append(ip)
db.close()

df = pd.DataFrame({'name': name_list, 'email': email_list, 'phone': phone_list, 'ip_network': ip_list, 'office':office_list})
# print(df)
df = df.groupby(['ip_network']).agg(lambda x: ','.join(x[x.notna()]))
# print(df)
## update data in school_net
data = configparser.ConfigParser()
data.read('config.ini')
host = data['tyrcDB']['HOST']
user = data['tyrcDB']['USER']
passwd = data['tyrcDB']['PASSWORD']
db = data['tyrcDB']['DB']
db = MySQLdb.connect(host, user, passwd, db, charset="utf8")

cursor = db.cursor()
update_cnt = 0
insert_cnt = 0
sql_list = []
except_ip = ['140.115.183.0/24', '140.115.184.0/24', '140.115.185.0/24','140.115.186.0/24','140.115.187.0/24']
for idx, row in df.iterrows():
    sql = "select ip_network from school_net where ip_network='"+idx+"';"
    cursor.execute(sql)
    if((idx not in except_ip) and len(row['office'].split(","))>1):
        row['office'] = row['office'].split(',')[0]
    if(cursor.rowcount!=0):
        sql = "update school_net set admin_contact='"+row['name']+"', admin_tel='"+row['phone']+"', admin_mail='"+row['email']+"', network_name='"+row['office']+" ' where ip_network='"+idx+"';"
        update_cnt += 1
    else:
        sql = "insert into school_net (admin_contact, admin_tel, admin_mail, ip_network, network_name, mail_notify, line_notify) values ('"+row['name']+"', '"+row['phone']+"','"+row['email']+"','"+row['office']+"','"+idx[1]+"', '1', '0');"
        insert_cnt += 1
    sql_list.append(sql)

    cursor.execute(sql)
    db.commit()
print("共更新{}筆資料, 新增{}筆資料".format(update_cnt, insert_cnt))
for sql in sql_list:
    print(sql)
db.close()
print("Update successfully!")

