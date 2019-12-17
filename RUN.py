import copy
from taskgen import StaffordRandFixedSum as genTaskRates
from taskgen import gen_periods as genTaskPeriods
import sys
import Servers.ServerEDF
import Servers.ServerDual
import Task.EDFTask

class RunScheduler:
    def pack(self,duals):
        bins = self.worstFitBins(duals)
        return self.convertBinsToServers(bins)  
    
    def convertBinsToServers(self,bins):
        servers = []
        for bin in bins:
            serverSet = []
            for dual in bin:
                serverSet.append(dual.convertToEDFServer())      
            servers.append(ServerEDF(serverSet, None, None))
        return servers
        
    def worstFitBins(self,duals):
        bins = []
        binSpaces = []
        bins.append([])
        for dual in duals:
            if(len(binSpaces) == 0):
                bins[0].append(dual)
                binSpaces.append(1-dual.getRate())
                
            index = self.getEmptiestBinIndex(binSpaces)
            #does not fit in emptiest bin
            if(binSpaces[index] < dual.getRate()):
                bins.append([dual])
                binSpaces.append(1-dual.getRate())
            else:
                bins[index].append(dual)
                binSpaces[index] -= dual.getRate()
        return bins
    
    def dual(self, servers):
        duals = []
        for server in servers:
            duals.append(ServerDual(server))
        return duals
    
    def getEmptiestBinIndex(self, binSpaces):
        min = binSpaces[0]
        minIndex = 0
        for ix, space in enumerate(binSpaces):
            if space < min:
                min = space
                minIndex = ix
        return minIndex
    
    def convertToSingletonServers(self,taskset):
        '''
        Taskset: list of tuples (rate, deadline)
        '''
        servers = []
        for task in taskset:
            singleton = ServerEDF(None, task[0], task[1])
            servers.append(singleton)
        return servers
        
    def reduceToUniserver(self, servers):
        while(len(servers) > 1):
            servers = self.dual(servers)
            servers = self.pack(servers)
            for server in servers:
                print(server)
            print()
        print("-------------------")

    def scheduleEDFServers(self, servers, time):

        for i in range(0, time):
            for server in servers:
                server.updateDeadline(time)



 

def printServers(servers):
    for server in servers:
        print(server)
if __name__ == "__main__":
    #generate 100 task sets with n tasks = 17
    
    nTasks = 17
    minPeriod = 5
    maxPeriod = 100
    periodGranularity = minPeriod
    nSets = 1
    
    for i in range(100, 105):
        rate = i/100
        taskRates = genTaskRates(nTasks, rate, nSets)
        taskPeriods = genTaskPeriods(nTasks, nSets, minPeriod, maxPeriod, minPeriod,"logunif")
        taskSet = []
        for ix,rate in enumerate(taskRates[0]):
            taskSet.append((rate, taskPeriods[0][ix]))
        scheduler = RunScheduler()
        servers = scheduler.convertToSingletonServers(taskSet)       
        scheduler.reduceToUniserver(servers)
            
    
    

        

