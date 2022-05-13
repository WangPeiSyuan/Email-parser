# !/usr/bin/python3
# coding: utf-8
import mailbox
import argparse
from utlis import *


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
            process(table, ip, id, date, subject, content, insert)

