import ipaddress
import MySQLdb
import configparser

data = configparser.ConfigParser()
data.read('/var/www/soc/config.ini')
print(data)
host = data['tyrcDB']['HOST']
user = data['tyrcDB']['USER']
passwd = data['tyrcDB']['PASSWORD']
db = data['tyrcDB']['DB']
db = MySQLdb.connect(host, user, passwd, db, charset="utf8")
cursor = db.cursor()

def isSubnet(ip, subnet):
    try:
        return ipaddress.IPv4Address(ip) in ipaddress.IPv4Network(subnet)
    except:
        return False

def smallest_domain(subnet_list):
    mask=[]
    mask=[subnet[2].split('/')[1] for subnet in subnet_list]
    max_value = max(mask)
    index = mask.index(max_value)
    return subnet_list[index]    

def getSubnet(ip):
    sql = "select * from school_net;"
    cursor.execute(sql)
    subnet_list=[]
    for row in cursor:
        subnet = row[2]
        if(isSubnet(ip, subnet)):
            subnet_list.append(row) 
    if(len(subnet_list)==0):
        return False, False, False, False, False, "none", False
    elif(len(subnet_list)==1):
        row=subnet_list[0]
    else: #multiple mask fit in ip need to find the smallest domain
        row = smallest_domain(subnet_list)        
    network_name = row[1]
    subnet = row[2]
    admin_mail = row[6]
    admin_line = row[4]
    mail_notify = row[7]
    line_notify = row[8]
    ewa_process = row[11]
    admin_mail = ''.join(admin_mail.split()) 

    return subnet, admin_mail, admin_line, mail_notify, line_notify, network_name, ewa_process

def insert2table(table, ip, id, date, event_type, content):
    if(table=="soc"):
        #insert into soc
        sql = "insert into soc (soc_id, soc_ip, soc_date, event_type, soc_content) VALUES (%s, %s, %s, %s, %s);"
    elif(table=="ewa"):
        sql = "insert into ewa (ewa_id, ewa_ip, ewa_date, event_type, ewa_content) VALUES (%s, %s, %s, %s, %s);"
    values = (id, ip, date, event_type, content)
    try:
        cursor.execute(sql, values)
        db.commit()
    
        #find subnet admin
        sql = "select * from school_net;"
        cursor.execute(sql)
        subnet_list=[]
        for row in cursor:
            subnet = row[2]
            if(isSubnet(ip, subnet)):
                subnet_list.append(row) 
        if(len(subnet_list)==0):
            return False, False, False, False, False, "none", False
        elif(len(subnet_list)==1):
            row=subnet_list[0]
        else: #multiple mask fit in ip need to find the smallest domain
            row = smallest_domain(subnet_list)    
        if(table=="soc"):
            sql = "update soc set soc_school='"+row[1]+"' where soc_id = '"+id+"';"
        elif(table=="ewa"):
            sql = "update ewa set ewa_school='"+row[1]+"' where ewa_id = '"+id+"';"
            
        cursor.execute(sql)
        db.commit()
        
        network_name = row[1]
        subnet = row[2]
        admin_mail = row[6]
        admin_line = row[4]
        mail_notify = row[7]
        line_notify = row[8]
        ewa_process = row[11]
        admin_mail = ''.join(admin_mail.split())  
        return subnet, admin_mail, admin_line, mail_notify, line_notify, network_name, ewa_process
    
    except:
        print(id, " already inserted!")
        return False, False, False, False, False, False, False

def checkID(table, id):
    if(table=="soc"):
        sql = "select * from soc where soc_id = '"+id+"';"
    elif(table=="ewa"):
        sql = "select * from ewa where ewa_id = '"+id+"';"
    cursor.execute(sql)
    print(sql)
    if(cursor.rowcount==0):
        return False
    else:
        return cursor.fetchone()
     
def verifyID(table, id, transit):
    if(table=="soc"):
        sql = "update soc set verify = %s, verify_time = %s where soc_id = '"+id+"';"
    elif(table=="ewa"):
        sql = "update ewa set verify = %s, verify_time = %s where ewa_id = '"+id+"';"
    print(sql)
    values=('1', int(transit))
    cursor.execute(sql, values)
    db.commit()


