import MySQLdb
import datetime 


def check():

    db = MySQLdb.connect("localhost", "root", "Tyrcncu0930!", "tyrcDB", charset="utf8")
    cursor = db.cursor()
    today = datetime.datetime.today()
    deldays = datetime.timedelta(days=7)
    day = str(today-deldays)
    sql = "select * from soc where create_date >= '"+day+"' order by create_date desc;"
    cursor.execute(sql)
    result = cursor.fetchall()
    print("soc:")
    for row in result:
        print(row[0], row[3], row[7])

    sql = "select * from ewa where create_date >= '"+day+"' order by create_date desc;"
    cursor.execute(sql)
    result = cursor.fetchall()
    print("ewa:")
    for row in result:
        print(row[0], row[3], row[7])

if __name__ == '__main__':
    check()

