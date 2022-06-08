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

    for idx, email_obj in enumerate(mbox_obj):
        email_data = GmailMboxMessage(email_obj)
        content, subject = email_data.parse_email()
        ip, date = parse_ip(str(content))
        if(ip):
            table, id = parse_title(str(subject)) #soc/ewa
        if(id == opt.id):  
            insert = False
            process(table, ip, id, date, subject, content, insert)
            break

