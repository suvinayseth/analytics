import psycopg2 #for psql 
import ast
import collections
from collections import defaultdict
import csv
import pdb #python debugger
import itertools #For looping on a dictionary
import subprocess #for running shell commands from within python
import datetime
from datetime import timedelta

#Connect to the psql database
psql_connect = psycopg2.connect("dbname=test1 host=10.1.9.12 port=5432 user=dev password=dev")
psql_cur = psql_connect.cursor()

#Define start month and year
start_month = 3
start_year = 2014

#current month to be extracted
effective_datetime = datetime.datetime.now() - timedelta(days=2)
current_month = str(effective_datetime.strftime('%m'))
current_year = str(effective_datetime.year)

def print_line(file_name):
    with open(file_name) as gsutil_file:
        next(gsutil_file)
        for line in gsutil_file:
            print 'insert into table_temp values ({0})'.format(line)

#Running shell commands
for year in xrange(start_year, effective_datetime.year) 
    for month in xrange(start_month, effective_datetime.strftime('%m')+1)
        try:
            file_name = "gs://pubsite_prod_rev_00028184847009703008/stats/installs/installs_com.locon.housing_"+current_year+current_month+"_overview.csv"
            p = subprocess.Popen("cd /home/dev/Suvinay/gsutil;\
                                gsutil cp " + file_name + " /home/dev/Suvinay/gsutil;",
                                 shell=True, stdout=subprocess.PIPE , stderr = subprocess.STDOUT)
        except:
            print "error with subprocess"
            
            #defining vm path to access file
        file_name = "/home/dev/Suvinay/gsutil/installs_com.locon.housing_" + year + month + "_overview.csv"

        print_line(file_name)
       



