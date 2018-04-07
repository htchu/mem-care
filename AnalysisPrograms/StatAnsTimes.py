import sqlite3
import sys
import csv

dbconn = sqlite3.connect('memtest.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
cursor = dbconn.cursor()
cursor.execute("SELECT Person, TestType, TestTime, TestGoal, Answer, AnsDuration FROM Test")
listPerson = ["TestA", "TestB", "TestC", "TestD", "TestE"]
count = {1:{"TestA":0, "TestB":0, "TestC":0, "TestA":0, "TestD":0, "TestE":0}, 
        -1:{"TestA":0, "TestB":0, "TestC":0, "TestA":0, "TestD":0, "TestE":0}, 
         0: {"TestA":0, "TestB":0, "TestC":0, "TestA":0, "TestD":0, "TestE":0}}
timespan = {1:{"TestA":0, "TestB":0, "TestC":0, "TestA":0, "TestD":0, "TestE":0}, 
        -1:{"TestA":0, "TestB":0, "TestC":0, "TestA":0, "TestD":0, "TestE":0}, 
         0: {"TestA":0, "TestB":0, "TestC":0, "TestA":0, "TestD":0, "TestE":0}}
countAll= {"TestA":0, "TestB":0, "TestC":0, "TestA":0, "TestD":0, "TestE":0}
total = 0
for row in cursor:
    #print (row)
    person = row[0]
    answer = row[4]
    span   = row[5]
    count[answer][person] += 1
    timespan[answer][person] += span
    countAll[person] +=1
    total += 1
dbconn.close()

#print(count)
#print(timespan)
with open('mem-times.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    csvwriter.writerow(['Count','Right','Wrong','No answer'])
    for i in range(len(listPerson)):
        p = listPerson[i]
        mul = total/countAll[p]
        csvwriter.writerow([p, count[1][p], count[-1][p], count[0][p]])
    csvwriter.writerow(['AvgTimes','Right','Wrong','No answer'])
    for i in range(len(listPerson)):
        p = listPerson[i]
        mul = total/countAll[p]
        csvwriter.writerow([p, timespan[1][p]/count[1][p], timespan[-1][p]/count[-1][p], timespan[0][p]/count[0][p]])
    csvwriter.writerow(['Ratio','Right','Wrong','No answer'])
    for i in range(len(listPerson)):
        p = listPerson[i]
        mul = total/countAll[p]
        csvwriter.writerow([p, count[1][p]/countAll[p], count[-1][p]/countAll[p], count[0][p]/countAll[p]])

