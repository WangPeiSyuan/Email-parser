import ipaddress
import MySQLdb

def isSubnet(ip, subnet):
    
    try:
        return ipaddress.IPv4Address(ip) in ipaddress.IPv4Network(subnet)
    except:
        return False

def getSubnet(ip):
    
    db = MySQLdb.connect("localhost", "root", "Tyrcncu0930!", "tyrcDB", charset="utf8")
    cursor = db.cursor()
    sql = "select * from school_net;"
    cursor.execute(sql)
    for row in cursor:
        subnet = row[1]
        if(isSubnet(ip, subnet)):
            admin_mail = row[5]
            return subnet, admin_mail
    return False, False

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
                return subnet, admin_mail
    except:
        db.close()
        print(id, " already inserted!")
        return False, False

    

def checkID(table, id):
    
    print("check table: ", table)
    if(table=="soc"):
        sql = "select * from soc where soc_id = '"+id+"';"
    elif(table=="ewa"):
        sql = "select * from ewa where ewa_id = '"+id+"';"
    cursor.execute(sql)
    if(cursor.rowcount==0):
        return False
    else:
        return True
     
