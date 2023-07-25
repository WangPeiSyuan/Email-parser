import MySQLdb
import datetime 
import configparser


def check():

    data = configparser.ConfigParser()
    data.read('/var/www/soc/config.ini')
    host = data['tyrcDB']['HOST']
    user = data['tyrcDB']['USER']
    passwd = data['tyrcDB']['PASSWORD']
    database = data['tyrcDB']['DB']
    db = MySQLdb.connect(host, user, passwd, database, charset="utf8")
    cursor = db.cursor()
    today = datetime.datetime.today()
    deldays = datetime.timedelta(days=14)
    day = str(today-deldays)
    sql = "select * from soc where create_date >= '"+day+"' order by create_date desc;"
    cursor.execute(sql)
    result = cursor.fetchall()
    print("soc:")
    for row in result:
        print(row[0], row[3], row[8])

    sql = "select * from ewa where create_date >= '"+day+"' order by create_date desc;"
    cursor.execute(sql)
    result = cursor.fetchall()
    print("ewa:")
    for row in result:
        print(row[0], row[3], row[8])

if __name__ == '__main__':
    check()

