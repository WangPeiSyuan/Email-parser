# !/usr/bin/python3
# coding: utf-8
import mailbox
import argparse
from utlis import *

DEBUG=True
parser= argparse.ArgumentParser()
parser.add_argument('--check', help='check before cleaning mailbox')
opt = parser.parse_args()

if __name__ == '__main__':
    mbox_obj = mailbox.mbox('/var/mail/soc')
    num_entries = len(mbox_obj)
    
    for idx, email_obj in enumerate(mbox_obj):
        print('##########parsing email {0} of {1}##############'.format(idx, num_entries))
        email_data = GmailMboxMessage(email_obj)
        content, subject = email_data.parse_email()
        print(subject)
        ip, date = parse_ip(content)
        if(ip):
            table, id = parse_title(subject) #soc/ewa
            print(ip, table)
        if(ip and table):
            insert=True
            if(opt.check):
                if(checkID(table, id)==False): #before cleaning mailbox, check if DB has the mail, if not insert it
                    process(table, ip, id, date, subject, content, insert)
                else:
                    print("ok")
            else:  
                process(table, ip, id, date, subject, content, insert)

