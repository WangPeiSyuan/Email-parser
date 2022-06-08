import os
import time
import pickle

f = open('/var/www/soc/ncu_admin/mail_content.txt', 'r')
content = f.read()
f = open('/var/www/soc/ncu_admin/admin_info.txt','r')
admin_info = f.read()
admin_info = admin_info.split(';')
admin_name = admin_info[0]
admin_mail = admin_info[1].rstrip()
now = time.ctime()
cmd = "LANG=ZH_TW.big5 && echo '"+content+"\n"+now+"' | mail -s 'mail test cmd ' -a 'From: "+admin_name+"<"+admin_mail+">' 110522127@cc.ncu.edu.tw, peistu13333@g.ncu.edu.tw,center15@cc.ncu.edu.tw,star01250125@gmail.com"

os.system(cmd)
print(cmd)
