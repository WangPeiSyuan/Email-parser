# !/usr/bin/python3
# coding: utf-8
import mailbox
import datetime
from utlis import *



if __name__ == '__main__':
    mbox_obj = mailbox.mbox('/var/mail/soc')
    num_entries = len(mbox_obj)
    today = datetime.datetime.today()
    deldays = datetime.timedelta(days=7)
    date7 = today-deldays
    last=0
    for idx, email_obj in mbox_obj.iteritems():
        print('##########parsing email {0} of {1}##############'.format(idx, num_entries))
        email_data = GmailMboxMessage(email_obj)
        content, subject = email_data.parse_email()
        ip, date = parse_ip(content)
        if(ip):
            table, id = parse_title(subject) #soc/ewa
        if(ip and table):
            result = checkID(table, id)
            if(result==False): #before cleaning mailbox, check if DB has the mail, if not insert it
                insert=True
                process(table, ip, id, date, subject, content, insert)
            
            result = checkID(table, id)
            result_date = result[7]
            if(result_date<date7):
                print("Deleting "+ subject, " ", result_date)
                last=idx

    for i in range(last+1):
        mbox_obj.remove(i)
    mbox_obj.flush()
    mbox_obj.close()
