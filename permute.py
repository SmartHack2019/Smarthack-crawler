import csv
import sys
import string
printable = set(string.printable)

import mysql.connector
import uuid
mydb = mysql.connector.connect(
  host="eu-cdbr-west-02.cleardb.net",
  user="ba980eb6f8bf25",
  passwd="7d9c388c",
  database="heroku_63117997832c3e6"
)
mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM companies")
myresult = mycursor.fetchall()

dictio = {}

for r in myresult:
    dictio[str(r[2]).upper()] = r[0]



csv.field_size_limit(100000000)
with open("data.csv", "r") as f:
    reader = csv.reader(f)
 
    data = list(reader)

    
data = [x for x in data if x != []]

print len(data)
i = 0
for d in data:
  i += 1
  print i
  if i%100 == 0:
    print i
    mydb.commit()
  if i == i%1000 == 0:
    break
    
  company_code = d[0].split('/')[-2]
  toadd = filter(lambda x: x in printable, d[1])
  mycursor.execute('INSERT INTO newses (Id, CompanyId, Link, Content) VALUES (%s, %s, %s, %s)', (str(uuid.uuid4()), dictio[company_code], d[0], toadd))
mydb.commit()
    
    






