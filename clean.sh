#!/bim/bash
rm /var/mail/soc
touch /var/mail/soc
chown soc:mail /var/mail/soc
chmod o-r /var/mail/soc
chmod g+rw /var/mail/soc
