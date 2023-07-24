# !/usr/bin/python3
# coding: utf-8
import mailbox
import base64
import parse
import bs4
from email.header import decode_header, make_header
import re
import MySQLdb
import os
import argparse
from connectDB import *
from sender import *
from email.utils import formataddr, parsedate
import time
import warnings
warnings.filterwarnings("ignore")

DEBUG=False  #若為True，多寄給管理員
SEND_EWA_FLAG=False #預設為False，如果是區網EWA信件都不寄送，若為True就會寄送給各單位管理員

def get_html_text(html):
    try:
        return bs4.BeautifulSoup(html, 'lxml').body.get_text(' ', strip=True)
    except AttributeError: # message contents empty
        return None

class GmailMboxMessage():
    def __init__(self, email_data):
        if not isinstance(email_data, mailbox.mboxMessage):
            raise TypeError('Variable must be type mailbox.mboxMessage')
        self.email_data = email_data

    def parse_email(self):
        email_labels = self.email_data['X-Gmail-Labels']
        email_date = self.email_data['Date']
        email_from = self.email_data['From']
        email_to = self.email_data['To']
        email_subject = self.email_data['Subject']
        try:
            email_subject = make_header(decode_header(email_subject))
        except:
            pass
           # print("email subject:", email_subject)
        email_text = self.read_email_payload()
        
        return str(email_text), str(email_subject) 
    
    def get_transit_time(self):
        email_date = self.email_data['Date']
        email_received = self.email_data['Received']
        received_t = parsedate(email_received.split(';')[1][1:])
        sent_t = parsedate(email_date)
        received_t = time.mktime(received_t)
        sent_t = time.mktime(sent_t)
        transit = received_t - sent_t
        return int(transit)
    
    def read_email_payload(self):
        email_payload = self.email_data.get_payload()
        if self.email_data.is_multipart():
            email_messages = list(self._get_email_messages(email_payload))
        else:
            email_messages = [email_payload]
        return self._read_email_text(email_messages[0])

    def _get_email_messages(self, email_payload):
        for msg in email_payload:
            if isinstance(msg, (list,tuple)):
                for submsg in self._get_email_messages(msg):
                    yield submsg
            elif msg.is_multipart():
                for submsg in self._get_email_messages(msg.get_payload()):
                    yield submsg
            else:
                yield msg

    def _read_email_text(self, msg):
        content_type = 'NA' if isinstance(msg, str) else msg.get_content_type()
        encoding = 'NA' if isinstance(msg, str) else msg.get('Content-Transfer-Encoding', 'NA')
        if 'text/plain' in content_type or 'text/html' in content_type:
            msg_text = msg.get_payload()
            if('base64' in encoding):
                msg_text = base64.b64decode(msg_text)
                msg_text = msg_text.decode("utf8","ignore")
        elif content_type == 'NA': #for non multipart mail
            try:
                msg_text = get_html_text(msg)
                msg_text = base64.b64decode(msg_text)
                msg_text = msg_text.decode("utf8", "ignore")
            except:
                msg_text = get_html_text(msg)
        return (msg_text)

def parse_ip(content):
    title = re.search('<td>事件主旨</td>.*<td>事件描述</td>', content)
    if(title): 
        ## parse ip
        ip = re.search( r'[0-9]+(?:\.[0-9]+){3}', title.group(0))
        if(ip):
            ## parse date      
            date = re.search("原發布時間</td><td width='380'>.*</td></tr><tr><td>事件類型</td>", content) 
            soup = bs4.BeautifulSoup(date.group(0),'html.parser')
            text = soup.get_text()
            date = re.sub('[\u4e00-\u9fa5]','',text)
            ## parse event type
            event_type = re.search("事件類型</td>.*原發現時間", content).group(0)
            event_type = re.search("<td>.*</td>",event_type).group(0)
            soup = bs4.BeautifulSoup(event_type,'html.parser')
            event_type = soup.get_text()
            
            return ip.group(0), date, event_type
            
    return False, False, False
def parse_title(subject):
    
    soc = re.search('事件單', subject)
    ewa = re.search('預警情報', subject)
    if(soc):
        soc_id = re.search("(事件單編號:.*)", subject)
        soc_id = re.findall('[a-zA-Z0-9\-]', soc_id.group(0))
        soc_id = ''.join(soc_id)
        #print("發布編號:", soc_id)
        return "soc", soc_id
    elif(ewa): 
        ewa_id = re.search("(發布編號:.*)", subject)
        ewa_id = re.findall('[a-zA-Z0-9\-]', ewa_id.group(0))
        ewa_id = ''.join(ewa_id)
        #print("發布編號:", ''.join(ewa_id))
        return "ewa", ewa_id
    return False, False

def process(table, ip, id, date, event_type, subject, content, insert):
    if(insert==True):
        data, to_mail, to_line, mail_no, line_no, network_name, ewa_process = insert2table(table, ip, id, date, event_type, content)
    else:
        data, to_mail, to_line, mail_no, line_no, network_name, ewa_process = getSubnet(ip)
    print("network name:", network_name)
    title = "[NEW]-教育機構資安通報-("+str(network_name)+str(ip)+")"+str(subject)
    print("data:", data)
   

    f = open('/var/www/soc/ncu_admin/mail_content.txt', 'r')
    header = f.read()
    f = open('/var/www/soc/ncu_admin/admin_info.txt','r')
    admin_info = f.read()
    admin_info = admin_info.split(';')
    if(data):
        if((table=="ewa") and ewa_process=='0'):         # 不是中央大學的EWA不會發
            print("ewa不通知")
            return False
        
        to_user=[]
        to_mail=''.join(to_mail.split())
        to_mail = to_mail.split(',')
        for user in to_mail:
            to_user.append(user)
        to_user.append("tyrc@ncu.edu.tw")
        
        to_chat=[]
        if(to_line):
            to_line=''.join(to_line.split())
            to_line = to_line.split(',')
            for chat in to_line:
                to_chat.append(chat)    
        if('140.115' in data):
            admin_name = admin_info[0]
            admin_mail = admin_info[1].rstrip()
            content = header+"<br>"+content
            #正式上線時會通知的管理員
            to_user = to_user + ['center2@cc.ncu.edu.tw', 'center25@cc.ncu.edu.tw','center24@cc.ncu.edu.tw','center20@cc.ncu.edu.tw','center15@cc.ncu.edu.tw','cym@cc.ncu.edu.tw'] 
        else: 
            admin_name = admin_info[2]
            admin_mail = admin_info[3].rstrip()

        from_user = formataddr((admin_name, admin_mail))
        if(DEBUG==True):
            content = str(to_user)+"<br>"+content
            #測試時通知的管理員
            to_user = ['peiswang824@gmail.com', '110522127@cc.ncu.edu.tw', 'center20@cc.ncu.edu.tw', 'center15@cc.ncu.edu.tw', ' tyrc@ncu.edu.tw']
        print("mail no:", mail_no, " line no:", line_no)
        if(mail_no=="1"):
            print("sending mail...")
            send_mail(content, to_user, from_user, title)
        if(line_no=="1"):
            print("sneding line...")
            send_line(title, to_chat)
        
        return True
    elif(network_name=="none" and ('140.115' in str(ip))):
        print(network_name)
        admin_name = admin_info[2]
        admin_mail = admin_info[3].rstrip()
        from_user = formataddr((admin_name, admin_mail))
        title = "[NEW]-教育機構資安通報-(請補正school net欄位"+str(ip)+")"+str(subject)
        to_user = ['peiswang824@gmail.com', 'center20@cc.ncu.edu.tw', 'center15@cc.ncu.edu.tw']
        send_mail(content, to_user, from_user, title)

