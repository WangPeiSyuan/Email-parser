# !/usr/bin/python3
# coding: utf-8
import mailbox
from utils import *


if __name__ == '__main__':
    mbox_obj = mailbox.mbox('/var/mail/soc')
    num_entries = len(mbox_obj)

    for idx, email_obj in enumerate(mbox_obj):
        email_data = GmailMboxMessage(email_obj)
        content, subject = email_data.parse_email()
        ip, date, event_type  = parse_ip(str(content))
        if(ip):
            table, id = parse_title(str(subject)) #soc/ewa
        if(ip and table):
            DB_data = checkID(table, id)
            if(DB_data):
                print("{} Mbox:{} DB:{} 一致".format(DB_data[1], id, DB_data[0]))
            else: 
                print("{} Mbox DB 不一致".format(id))
    print("done")
                
                        

