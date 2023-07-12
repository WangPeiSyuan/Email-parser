# !/usr/bin/python3
# coding: utf-8
import mailbox
import argparse
from utils import *

parser = argparse.ArgumentParser()
parser.add_argument('--id', help='id for soc_id/ewa_id', required=True)
opt = parser.parse_args()


if __name__ == '__main__':
    mbox_obj = mailbox.mbox('/var/mail/soc')
    num_entries = len(mbox_obj)
    send = False
    for idx, email_obj in enumerate(mbox_obj):
        email_data = GmailMboxMessage(email_obj)
        content, subject = email_data.parse_email()
        ip, date, event_type  = parse_ip(str(content))
        if(ip):
            table, id = parse_title(str(subject)) #soc/ewa
        if(id == opt.id):  
            insert = False
            # process(table, ip, id, date, event_type, subject, content, insert)
            send = True
            print("{} 寄送成功".format(id))
            break
    if(send == False):
        print("寄送失敗，信箱只保留7天內信件，此信已不存於信箱")

