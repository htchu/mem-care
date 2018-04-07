import sqlite3
import sys
import csv
import numpy

dbconn = sqlite3.connect('memtest.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
cursor = dbconn.cursor()
cursor.execute("SELECT Person, TestType, TestTime, TestGoal, Answer, AnsDuration FROM Test")

mp = {"TestA":0, "TestB":1, "TestC":2, "TestD":3, "TestE":4}   #map testee persons to array indixes
mpi = {0:"TestA", 1:"TestB", 2:"TestC", 3:"TestD", 4:"TestE"}  #map array indixes to testee person
tt = {"singer1":0, "singer2":1, "song1":2, "song2":3}          #map test types to array indixes
tti = {0:"singer1", 1:"singer2", 2:"song1", 3:"song2"}         #map array indixes to test types
tg = {1:0,2:1,3:2,4:3,5:4}                                     #offset of row indices
aa = {1:2, -1:0, 0:1}                                          #offset of answers 

numpy.zeros((5, 5))
Mat = [[[[0 for a in range(3)] for z in range(5)] for y in range(4)] for x in range(5)]
All =  [[[0                    for z in range(5)] for y in range(4)] for x in range(5)]
YN =   [[[0                    for z in range(5)] for y in range(4)] for x in range(5)]
totalYN = 0
total = 0
for row in cursor:
    #print (row)
    person = mp[row[0]]
    ttype  = tt[row[1]]
    tgoal  = tg[row[3]]
    answer = aa[row[4]]
    Mat[person][ttype][tgoal][answer] += 1
    All[person][ttype][tgoal] += 1
    if answer !=1:
        YN[person][ttype][tgoal] += 1
        totalYN +=1
    total +=1
dbconn.close()
print(totalYN)
print(total)
       
with open('mem-stat.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    csvwriter.writerow(['Person','TestType','TestGoal', 'Yes/No'])

    for y in range(4):
        for z in range(5):
            for x in range(5):
                if (Mat[x][y][z][2] >= Mat[x][y][z][0]) and (Mat[x][y][z][2] > 0):
                    csvwriter.writerow([mpi[x], tti[y], z+1, 'O'])
                else:
                    csvwriter.writerow([mpi[x], tti[y], z+1, 'X'])