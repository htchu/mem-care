import sqlite3
import sys
import csv
import numpy

dbconn = sqlite3.connect('memtest.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
cursor = dbconn.cursor()
cursor.execute("SELECT Person, TestType, TestTime, TestGoal, Answer, AnsDuration FROM Test")
mp = {"TestA":0, "TestB":1, "TestC":2, "TestD":3, "TestE":4}
mpi = {0:"TestA", 1:"TestB", 2:"TestC", 3:"TestD", 4:"TestE"}
tt = {"singer1":0, "singer2":1, "song1":2, "song2":3}
tti = {0:"singer1", 1:"singer2", 2:"song1", 3:"song2"}
tg = {1:0,2:1,3:2,4:3,5:4}
aa = {1:2, -1:0, 0:1}
# Creates a list containing 5 lists, each of 8 items, all set to 0
# for word in words:
'''
w, h = 8, 5
Matrix = [[0 for x in range(w)] for y in range(h)] 
Matrix[0][6] = 3 # valid
Matrix[h][w] = 3 # valid
'''
numpy.zeros((5, 5))
Mat = [[[[0 for a in range(3)] for z in range(5)] for y in range(4)] for x in range(5)]
All =  [[[0                    for z in range(5)] for y in range(4)] for x in range(5)]
total = 0
for row in cursor:
    #print (row)
    person = mp[row[0]]
    ttype  = tt[row[1]]
    tgoal  = tg[row[3]]
    answer = aa[row[4]]
    Mat[person][ttype][tgoal][answer] += 1
    All[person][ttype][tgoal] += 1
    total +=1
dbconn.close()

print(total)
#print(timespan)
#print the answer count for each problem
with open('mem-counts.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    csvwriter.writerow(['Person','TestType','TestGoal', 'Answer','Count'])
    for x in range(5):
        for y in range(4):
            for z in range(5):
                for a in range(3):
                    csvwriter.writerow([mpi[x], tti[y], z+1, a-1, Mat[x][y][z][a]])
    