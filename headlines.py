import csv
import mysql.connector


mydb = mysql.connector.connect(
  host="eu-cdbr-west-02.cleardb.net",
  user="ba980eb6f8bf25",
  passwd="7d9c388c",
  database="heroku_63117997832c3e6"
)
mycursor = mydb.cursor()


with open('links.csv', 'r') as f:
    reader = csv.reader(f)
    data = list(reader)


print len(data)
i = 0
for d in data:
    if i % 100 == 0:
        mydb.commit()
    i+=1
    print i
    mycursor.execute("UPDATE newses SET Headline=%s WHERE Link=%s", (d[1], d[2]))

mydb.commit()