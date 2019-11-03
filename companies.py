import csv
import sys
from random import random


import mysql.connector
import uuid
mydb = mysql.connector.connect(
  host="eu-cdbr-west-02.cleardb.net",
  user="ba980eb6f8bf25",
  passwd="7d9c388c",
  database="heroku_63117997832c3e6"
)
mycursor = mydb.cursor()
csv.field_size_limit(100000000)

with open('companies.csv', 'r') as f:
    reader = csv.reader(f)
    data = list(reader)

data = [x for x in data if x != []]

for d in data:
    mycursor.execute('INSERT INTO companies (Id, Code, Name, Price, Increase, Percent) VALUES(%s, %s, %s, 0, 0, 0)', (str(uuid.uuid4()), d[0], d[1]))

mydb.commit()