import MySQLdb
## get data from sysmgrdb and preprocess 
HOST="140.115.17.196"
DATABASE="sysmgrdb"
USER="tyrc_ncu"
PASSWORD="Merry34!"

db = MySQLdb.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
cursor = db.cursor()
sql = "select name,email,phone,faculty.did,ip_range from faculty join dept on faculty.did=dept.did" ##排除電算中心人員，因人員太多異動頻繁
cursor.execute(sql)

ip_list=[]
for row in cursor:    
    network = row[4].split(':')
    # print(network)
    for seg in network:
        if(seg!=''):
            if('/' in seg):
                ip = '140.115.'+seg
            else:
                ip = '140.115.'+seg+'.0/24'
            ip_list.append(ip)

sql = "select std_name,email,phone,student.did,ip_range from student join dept on student.did=dept.did;" ##網管
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

            ip_list.append(ip)
db.close()
ip_list = list(set(ip_list))
# print(len(ip_list))
db = MySQLdb.connect("localhost", "root", "Tyrcncu0930!", "tyrcDB", charset="utf8")
cursor = db.cursor()
sql = "select ip_network from school_net;"
cursor.execute(sql)
print("school net DB網段，但不存在於SNMG DB")
for row in cursor:
    ip = row[0]
    if('140.115' in ip):
        if(ip not in ip_list):
            print(ip)
db.close()
