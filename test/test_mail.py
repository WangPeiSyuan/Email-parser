import os
import time
import pickle
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
import MySQLdb

def mail_function(msg, to_user, from_user, title):
    message = MIMEMultipart()
    mail = MIMEText(msg,"html","utf-8")
    message.attach(mail)
    message["Subject"] = title
    message["From"] = from_user
    message['To'] = ", ".join(to_user)
    smtp_server = "localhost"
    smtp_port = 25
    server = smtplib.SMTP(smtp_server,smtp_port)
    #server.login(from_user,"")
    server.sendmail(from_user,to_user,message.as_string())
    server.quit()
    
db = MySQLdb.connect("localhost", "root", "Tyrcncu0930!", "tyrcDB", charset="utf8")
cursor = db.cursor()
sql = "select * from school_net where network_name='test';"
cursor.execute(sql)
for row in cursor:
    mail_to=row[5]

f = open('/var/www/soc/ncu_admin/mail_content.txt', 'r')
content = f.read()
f = open('/var/www/soc/ncu_admin/admin_info.txt','r')
admin_info = f.read()
admin_info = admin_info.split(';')
admin_name = admin_info[0]
admin_mail = admin_info[1].rstrip()
#to_user = ['peistu13333@g.ncu.edu.tw','110522127@cc.ncu.edu.tw','center20@cc.ncu.edu.tw','center15@cc.ncu.edu.tw']
#print(to_user)
to_user="peistu13333@g.ncu.edu.tw,"
to_user = to_user.split(',')
to_list=[]
for user in to_user:
    to_list.append(str(user))
#to_list.append("tyrc@ncu.edu.tw")
print(to_list)
content = ''.join(to_list)+"<br>"+content
from_user = formataddr((admin_name, admin_mail))

mail_function(content, to_list
        , from_user, "mail test")
