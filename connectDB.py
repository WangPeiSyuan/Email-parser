import ipaddress
import MySQLdb

def isSubnet(ip, subnet):
    
    try:
        return ipaddress.IPv4Address(ip) in ipaddress.IPv4Network(subnet)
    except:
        return False

def smallest_domain(subnet_list):
    mask=[]
    mask=[subnet[1].split('/')[1] for subnet in subnet_list]
    max_value = max(mask)
    index = mask.index(max_value)
    #print(subnet_list[index])
    return subnet_list[index]    

def getSubnet(ip):
  
    db = MySQLdb.connect("localhost", "root", "Tyrcncu0930!", "tyrcDB", charset="utf8")
    cursor = db.cursor()
    sql = "select * from school_net;"
    cursor.execute(sql)
    subnet_list=[]
    for row in cursor:
        subnet = row[1]
        if(isSubnet(ip, subnet)):
            print(row)
            subnet_list.append(row)    
    if(len(subnet_list)==0):
        return False, False, False, False, False
    elif(len(subnet_list)==1):
        row=subnet_list[0]
    else: #multiple mask fit in ip need to find the smallest domain
        row = smallest_domain(subnet_list)        
    subnet = row[1]
    admin_mail = row[5]
    admin_line = row[3]
    mail_notify = row[6]
    line_notify = row[7]
    
    return subnet, admin_mail, admin_line, mail_notify, line_notify

def insert2table(table, ip, id, date, content):
    
    db = MySQLdb.connect("localhost", "root", "Tyrcncu0930!", "tyrcDB", charset="utf8")
    cursor = db.cursor()
    if(table=="soc"):
        #insert into soc
        sql = "insert into soc (soc_id, soc_ip, soc_date, soc_content) VALUES (%s, %s, %s, %s);"
    elif(table=="ewa"):
        sql = "insert into ewa (ewa_id, ewa_ip, ewa_date, ewa_content) VALUES (%s, %s, %s, %s);"
    values = (id, ip, date, content)
    try:
        cursor.execute(sql, values)
        db.commit()
    
        #find subnet admin
        print("inserting:", id)
        sql = "select * from school_net;"
        cursor.execute(sql)
        for row in cursor:
            subnet = row[1]
            if(isSubnet(ip, subnet)):
                if(table=="soc"):
                    sql = "update soc set soc_school='"+row[0]+"' where soc_id = '"+id+"';"
                elif(table=="ewa"):
                    sql = "update ewa set ewa_school='"+row[0]+"' where ewa_id = '"+id+"';"
                cursor.execute(sql)
                db.commit()
                
                admin_mail = row[5]
                admin_line = row[3]
                mail_notify = row[6]
                line_notify = row[7]
                return subnet, admin_mail, admin_line, mail_notify, line_notify
    except:
        db.close()
        print(id, " already inserted!")
        return False, False, False, False, False

    

def checkID(table, id):
    
    db = MySQLdb.connect("localhost", "root", "Tyrcncu0930!", "tyrcDB", charset="utf8")
    cursor = db.cursor()
    if(table=="soc"):
        sql = "select * from soc where soc_id = '"+id+"';"
    elif(table=="ewa"):
        sql = "select * from ewa where ewa_id = '"+id+"';"
    cursor.execute(sql)
    if(cursor.rowcount==0):
        return False
    else:
        return True
     
def verifyID(table, id):
    
    db = MySQLdb.connect("localhost", "root", "Tyrcncu0930!", "tyrcDB", charset="utf8")
    cursor = db.cursor()
    if(table=="soc"):
        sql = "update soc set verify='1' where soc_id = '"+id+"';"
    elif(table=="ewa"):
        sql = "update ewa set verify='1' where ewa_id = '"+id+"';"
     
    cursor.execute(sql)
    db.commit()
    db.close()
ip = '120.124.30.82'
getSubnet(ip)
