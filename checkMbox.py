# -*- coding: utf-8 -*-
import mailbox
import base64
import parse
import bs4
from email.header import decode_header, make_header
import re

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
        email_subject = make_header(decode_header(email_subject))
        email_text = self.read_email_payload() 
        return email_text, email_subject 
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

'''
def parse_title(subject, table):
    if(table=='soc'):
        soc = re.search('事件單', subject)
        if(soc):
            print(subject)
    elif(table=='ewa'): 
        ewa = re.search('預警情報', subject)
        if(ewa):
            print(subject) 
'''
def parse_ip(content):
    title = re.search('<td>事件主旨</td>.*<td>事件描述</td>', content)
    if(title): 
        ## parse ip
        ip = re.search( r'[0-9]+(?:\.[0-9]+){3}', title.group(0))
        #return ip 

        if(ip):
            ## parse date      
            date = re.search("原發布時間</td><td width='380'>.*</td></tr><tr><td>事件類型</td>", content) 
            soup = bs4.BeautifulSoup(date.group(0),'html.parser')
            text = soup.get_text()
            date = re.sub('[\u4e00-\u9fa5]','',text)
            #print("發布時間:", date)
            
            return ip.group(0)

    return  False

if __name__ == '__main__':
    mbox_obj = mailbox.mbox('/var/mail/soc')
    num_entries = len(mbox_obj)

    for idx, email_obj in enumerate(mbox_obj):
        email_data = GmailMboxMessage(email_obj)
        content, subject = email_data.parse_email()
        ip = parse_ip(str(content))
        if(ip):
            print(str(subject))

