from api import data_generator
import numpy as np
import datetime
import pymysql

select_all = '''select * from moveset; '''
add_row = ''' insert into moveset (day, running, walking,jogging,cycling) values ("%s", %d, %d,%d, %d)'''
fetch_day='''select * from moveset where day='%s'; '''
update_move='''update moveset set %s=%d where day='%s' '''
fetch_month='''select SUM(running),SUM(walking),SUM(jogging),SUM(cycling) from moveset where YEAR(day)=%d AND MONTH(day)=%d'''
select_day='''select SUM(running),SUM(walking),SUM(jogging),SUM(cycling) from moveset where YEAR(day)=%d AND MONTH(day)=%d AND DAY(day)=%d'''
fetch_year='''select SUM(running),SUM(walking),SUM(jogging),SUM(cycling) from moveset where YEAR(day)=%d '''
'''
Queries used for interaction with moveset database
User Reader is set up to only have permission to Select,Insert and Update moveTracker database
'''

#Insert new date to table, used only for immediate operation, not abled on api path seperately
def update_db():
    conn = pymysql.connect(host="localhost",port= 3306, user="Reader", password="password",  database="moveTracker")
    for samples in data_generator():
        timestamp = datetime.datetime.now().date().strftime("%Y-%m-%d")
        with conn.cursor() as cursor:
            cursor.execute(add_row % (timestamp, 50, 20,10,3))
        conn.commit()
        print("row added")
#checking out all data
def get_entire_table():
    conn = pymysql.connect(host="localhost",port=3306, user="Reader", password="password", database="moveTracker")
    with conn.cursor() as cursor:
        cursor.execute(select_all)
        table = cursor.fetchall()
        print(len(table))
        return table
# Adds one minute of movement to a days movement data depending on activity label, creating new row if day's data didn't exist.
def update_day_data(activity):
    conn = pymysql.connect(host="localhost",port= 3306, user="Reader", password="password", database="moveTracker")
    with conn.cursor() as cursor:
        cursor.execute(fetch_day % datetime.datetime.now().date().strftime("%Y-%m-%d") )
        row=cursor.fetchone()
        print(row)
        if row==None:
            row=["NewData",0,0,0,0]
        new_minute=0
        if activity=="running":
            new_minute=row[1]+1
        if activity=="walking":
            new_minute=row[2]+1
        if activity=="jogging":
            new_minute=row[3]+1
        if activity=="cycling":
            new_minute=row[4]+1
        if row[0]=="NewData":
            row[0]=datetime.datetime.now().date().strftime("%Y-%m-%d")
            cursor.execute(add_row % (row[0],row[1],row[2],row[3],row[4]))
            conn.commit()
            return update_day_data(activity)
        cursor.execute(update_move % (activity,new_minute,datetime.datetime.now().date().strftime("%Y-%m-%d")))
        conn.commit()
        return "Row updated"

#selecting latest record, not used for debugging only
def get_latest_row():
    conn = pymysql.connect(host="localhost",port= 3306, user="Reader", password="password", database="moveTracker")
    with conn.cursor() as cursor:
        cursor.execute(select_last_row)
        row = cursor.fetchone()
        return row
#Fetching todays data, not used debugging only
def fetch_today():
    conn = pymysql.connect(host="localhost",port= 3306, user="Reader", password="password", database="moveTracker")
    with conn.cursor() as cursor:
        print(fetch_day % datetime.datetime.now().date().strftime("%Y-%m-%d"))
        cursor.execute(fetch_day % datetime.datetime.now().date().strftime("%Y-%m-%d") )
        row=cursor.fetchall()
        return row
#Fetching data for a specific month requiring entry of year and month parameter
def get_month(year,month):
    conn = pymysql.connect(host="localhost",port= 3306, user="Reader", password="password", database="moveTracker")
    with conn.cursor() as cursor:
        cursor.execute(fetch_month % (year,month))
    data=cursor.fetchall()
    return data
#Fetching data for a specific day requiring entry of year and month and day parameter
def get_day(year,month,day):
    conn = pymysql.connect(host="localhost",port= 3306, user="Reader", password="password", database="moveTracker")
    with conn.cursor() as cursor:
        cursor.execute(select_day % (year,month,day))
    data=cursor.fetchone()
    return data
#Fetching data for a specific year requiring entry of year
def get_year(year):
    conn = pymysql.connect(host="localhost",port= 3306, user="Reader", password="password", database="moveTracker")
    with conn.cursor() as cursor:
        cursor.execute(fetch_year % (year))
    data=cursor.fetchall()
    return data

#if __name__ == "__main__":
    #get_entire_table()