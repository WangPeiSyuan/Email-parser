# !/usr/bin/python3
# coding: utf-8
import mailbox
from utlis import *
from connectDB import checkID, verifyID

if __name__ == '__main__':
    mbox_obj = mailbox.mbox('/var/mail/verify')
    num_entries = len(mbox_obj)

    for idx, email_obj in enumerate(mbox_obj):
        print('##########parsing email {0} of {1}##############'.format(idx, num_entries))
        email_data = GmailMboxMessage(email_obj)
        content, subject = email_data.parse_email()
        
        ip, date = parse_ip(str(content))
        if(ip):
            table, id = parse_title(str(subject)) #soc/ewa
        if(ip and table):
            if(checkID(table, id)):
                transit_t = email_data.get_transit_time()
                print("transit time:", transit_t)
                verifyID(table, id, transit_t)
