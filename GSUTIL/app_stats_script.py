import psycopg2 #for psql 
import collections
from collections import defaultdict
import csv
import pdb #python debugger
import itertools #For looping on a dictionary
import subprocess #for running shell commands from within python
import datetime
from datetime import timedelta
from monthdelta import monthdelta
import sys

#Connect to the psql database
psql_connect = psycopg2.connect("dbname=test1 host=10.1.9.12 port=5432 user=dev password=dev")
psql_cur = psql_connect.cursor()

#Define start month and year
start_month = 5
start_year = 2014
aux_start_date = datetime.date(year=start_year, month=start_month, day=1)
#current year, month and day to be extracted
effective_datetime = datetime.datetime.now() - timedelta(days=2)
current_month = effective_datetime.month
current_year = effective_datetime.year
aux_end_date = datetime.date(year=current_year, month=current_month, day=1)
num_months = (aux_end_date.year-aux_start_date.year)*12+(aux_end_date.month-aux_start_date.month)
#Running shell commands
for i in range(num_months+1) :
    aux_date = aux_start_date + monthdelta(i)
    year = aux_date.year
    month = aux_date.strftime('%m')
    print year,month
    try:
        file_name = "gs://pubsite_prod_rev_00028184847009703008/stats/installs/installs_com.locon.housing_"+str(year)+month+"_overview.csv"
        p = subprocess.Popen("cd /home/dev/Suvinay/gsutil; gsutil cp " + file_name + " /home/dev/Suvinay/gsutil/.", shell=True, stdout=subprocess.PIPE , stderr = subprocess.STDOUT)
        p.wait()
    except:
        print "error with subprocess"
        
    #defining vm path to access file
    file_name = "/home/dev/Suvinay/gsutil/installs_com.locon.housing_" + str(year) + month + "_overview.csv"
    gsutil_file = open(file_name,mode='r')
    gsutil_text = gsutil_file.read().decode('utf-16le')
    gsutil_text = gsutil_text.split('\n')
    for line in gsutil_text[1:]:
        if line:
            values = line.split(',')
            date = int(values[0].replace('-',''))
            current_device_installs = int(values[2])
            daily_device_installs = int(values[3])
            daily_device_uninstalls = int(values[4])
            daily_device_upgrades = int(values[5])
            current_user_installs = int(values[6])
            total_user_installs = int(values[7])
            daily_user_installs = int(values[8])
            daily_user_uninstalls = int(values[9])
            print 'executing sql statement' 
            psql_cur.execute('INSERT into android_app_data values (%s,%s,%s,%s,%s,%s,%s,%s,%s)'%(date,daily_device_installs,current_device_installs,daily_user_installs,current_user_installs, total_user_installs,daily_device_uninstalls, daily_user_uninstalls,daily_device_upgrades))
               
psql_connect.commit()
