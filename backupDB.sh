DATE="`date +\%Y\%m\%d`"
SQLFILE=/var/log/mysql/backup/school_net_${DATE}.sql
DATABASE=tyrcDB
TABLE=school_net
USER=root
PASSWORD=Tyrcncu0930!

mysqldump -u ${USER} -p${PASSWORD} ${DATABASE} ${TABLE}> ${SQLFILE}
