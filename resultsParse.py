'''
takes in a raw results csv with format
    searchid,init time, final time,numHops,lastUpeer,url
and produces a csv file with format
searchid,avgTime,MaxTime,avgHops,MaxHops,MaxHopsUP
    with filename p + rawdataname


'''

import os,sys
import csv


class datum:
    def __init__(self,time,hops,hopUP):
        self.maxTime = time
        self.maxHops = hops
        self.maxUP = hopUP
        self.num = 1
        self.sumTime = time
        self.sumHops = hops
    def add(self,time,hops,hopUP):
        self.sumTime = self.sumTime + time
        self.sumHops = self.sumHops + hops
        self.num = self.num + 1
        if time > self.maxTime:
            self.maxTime = time
        if hops > self.maxHops:
            self.maxHops = hops
            self.maxUP = hopUP
    def compute(self):
        self.avgTime = self.sumTime / self.num
        self.avgHops = float(self.sumHops) / self.num
        


file = csv.reader(open(sys.argv[1],"r"))
data = {}
for row in file:
    if data.has_key(row[0]):
        data[row[0]].add(float(row[2]) - float(row[1]),int(row[3]),int(row[4]))
    else:
        data[row[0]] = datum(float(row[2]) - float(row[1]),int(row[3]),int(row[4]))
    
outFile = open('p'+sys.argv[1], "wt")
outWriter = csv.writer(outFile)

for key,item in data.items():
    item.compute()
    outWriter.writerow([key,item.avgTime,item.maxTime,item.avgHops,item.maxHops,item.maxUP])

outFile.close()





