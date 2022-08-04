import mysql.connector
import datetime
from datetime import date
import socket

status = True

# mysql server (DataBase)
mysql = mysql.connector.connect(
    host = "127.0.0.1",
    user = "root",
    password = "root",
    database = "Tracking_Record",
    port = 8889
)
cursor = mysql.cursor(buffered=True)

# fix variable
enter = "IN"
leave = "OUT"

while status == True:

    # current date
    date = datetime.datetime.now()
    created_at = datetime.datetime.now()

    # location (get current location from host name)
    lc = socket.gethostname()

    # user input 
    user_input = input()

    # pull data from DataBase 1 
    sql = f"SELECT * FROM student_info WHERE MC={user_input}"
    cursor.execute(sql)
    ID = cursor.fetchone()

    # breaking down variable pulled from DataBase 1
    stu_id, name, year, micode = ID

    # select user that match with describsion (user input, today, descending order)
    cursor.execute(f"SELECT * FROM get_insert \
            WHERE micode={user_input} and date=current_date and location='{lc}' \
                ORDER BY created_at DESC")
    cf = cursor.fetchone()

    # push data back to DataBase 2 for storing
    query_enter = f"INSERT INTO get_insert (id, name, year, location, status, date, micode) \
            VALUES ({stu_id},'{name}','{year}','{lc}','{enter}','{date}',{micode})"
    query_leave = f"INSERT INTO get_insert (id, name, year, location, status, date, micode) \
            VALUES ({stu_id},'{name}','{year}','{lc}','{leave}','{date}',{micode})"

    # if condition to check for IN/OUT
    if cf == None:
        cursor.execute(query_enter)
    else:
        if cf[4] == 'IN':
            cursor.execute(query_leave)
        else:
            cursor.execute(query_enter)    
    mysql.commit()

# close loop and DataBase
status = False
mysql.close()
