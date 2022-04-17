# -*- coding: utf-8 -*-
import mailbox
from utlis import *

if __name__ == '__main__':
    mbox_obj = mailbox.mbox('/var/mail/soc')
    num_entries = len(mbox_obj)

    for idx, email_obj in enumerate(mbox_obj):
        email_data = GmailMboxMessage(email_obj)
        content, subject = email_data.parse_email()
        ip, date = parse_ip(str(content))
        if(ip):
            print(str(subject)," ", date)

