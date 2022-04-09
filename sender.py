#!/usr/bin/python
#coding:utf-8
import smtplib 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests

def send_mail(msg, to_user, from_user, title):
    message = MIMEMultipart()
    mail = MIMEText(msg,"html","utf-8")
    message.attach(mail)
    message["Subject"] = title
    message["From"] = from_user
    message["To"] = ", ".join(to_user)
    smtp_server = "localhost"
    smtp_port = 25
    server = smtplib.SMTP(smtp_server,smtp_port)
    #server.login(from_user,"") 
    server.sendmail(from_user,to_user,message.as_string())
    server.quit()

def send_line(msg, token):
    #token = 'W4elJYcjhNG6oNypWwMR2r4rS8APoHv8ih5jtcuV5P1'

    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type" : "application/x-www-form-urlencoded"
    }

    payload = {'message': msg}
    r = requests.post("https://notify-api.line.me/api/notify", headers = headers, params = payload)
