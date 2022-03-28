#!/usr/bin/python
#coding:utf-8
import smtplib 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def mail_function(msg, to_user, from_user, title):
    message = MIMEMultipart()
    mail = MIMEText(msg,"html","utf-8")
    message.attach(mail)
    message["Subject"] = title
    message["From"] = from_user
    message["To"] = to_user
    smtp_server = "localhost"
    smtp_port = 25
    server = smtplib.SMTP(smtp_server,smtp_port)
    #server.login(from_user,"") 
    server.sendmail(from_user,to_user,message.as_string())
    server.quit()
