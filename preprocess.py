import MySQLdb

data = configparser.ConfigParser()
data.read('/var/www/soc/config.ini')
host = data['tyrcDB']['HOST']
user = data['tyrcDB']['USER']
passwd = data['tyrcDB']['PASSWORD']
db = data['tyrcDB']['DB']
db = MySQLdb.connect(host, user, passwd, db, charset="utf8")
cursor = db.cursor()

str=""
data=[]
with open('rwhois_tyc.txt') as f:
    while line := f.readline():
        if("---" not in line and line !=""):
            info = line.split(":")[1]
            str=str+info.strip()+";"
        elif("---" in line and len(str)!=0):
            data.append(str[:-1]+"\n")
            str=""

f.close()

for line in data:
    var = line.split(";")
    sql = "insert into school_net (network_name, ip_network, admin_contact, admin_tel, update_by) VALUES (%s, %s, %s, %s, %s);"
    values = (var[0], var[1], var[2], var[4], var[5])
    cursor.execute(sql, values)
    db.commit()

db.close()





