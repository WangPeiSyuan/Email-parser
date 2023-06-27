#!/bin/bash
python3 /var/www/soc/clean.py  > /var/www/soc/log/clean-`date +\%Y\%m\%d\%H\%M`.log 2>&1
chown soc:mail /var/mail/soc
chmod o+r /var/mail/soc
chmod g+rw /var/mail/soc
