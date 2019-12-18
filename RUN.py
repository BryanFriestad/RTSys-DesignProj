import copy
from taskgen import StaffordRandFixedSum as genTaskRates
from taskgen import gen_periods as genTaskPeriods
import sys
import Servers
import Task

def lessThan(a, b):
    if(a > b or abs(a-b) < 0.0001):
        return False
    else:
        return True
def printServers(servers):
    for server in servers:
        print(server)

def printTree(server):
    if(len(server.getClients()) == 0):
        print()
        print("leaf: " + str(server))
        return
    for client in server.getClients():
        printTree(client)
        print("Parent: " + str(server))


class RunScheduler:
    def pack(self,servers):
        bins = self.worstFitBins(servers)
        return self.convertBinsToServers(bins)  
    
    def convertBinsToServers(self,bins):
        servers = []
        for bin in bins:
            serverSet = []
            for server in bin:
                serverSet.append(server)  
            servers.append(Servers.ServerEDF(serverSet, None, None, serverType="packed"))
        return servers
        
    def worstFitBins(self,servers):
        bins = []
        binSpaces = []
        bins.append([])
        for server in servers:
            if(len(binSpaces) == 0):
                bins[0].append(server)
                binSpaces.append(1-server.getRate())
                continue
            index = self.getEmptiestBinIndex(binSpaces)
            #does not fit in emptiest bin
            if(lessThan(binSpaces[index],server.getRate())):
                bins.append([server])
                binSpaces.append(1-server.getRate())
            else:
                bins[index].append(server)
                binSpaces[index] = binSpaces[index] - server.getRate()
        return bins

    def getEmptiestBinIndex(self, binSpaces):
        maxS = 0
        minIndex = 0
        for ix, space in enumerate(binSpaces):
            if space > maxS:
                maxS = space
                minIndex = ix
        return minIndex
    
    def dual(self, servers):
        duals = []
        for server in servers:
            dual = Servers.ServerEDF(server.getClients(), 
                                     1-server.getRate(), 
                                     server.getDeadline(), 
                                     serverType="dual")
            duals.append(dual)

        return duals
    
    
    
    def convertToSingletonServers(self,taskset):
        '''
        Taskset: list of tuples (rate, deadline)
        '''
        servers = []
        for task in taskset:
            singleton = Servers.ServerEDF([], task[0], task[1])
            servers.append(singleton)
        return servers
        
    def reduceToUniserver(self, servers):
        serversC = servers
        count = 0
        while(len(servers) > 1):
            servers = self.pack(servers)
            if(len(servers) == 1): return servers,serversC
            servers = self.dual(servers)
        return servers, serversC

    def buildServerTree(self, server):

        clients = server.getClients()
        for client in clients:
            client.parent = server
            if client.hasClients():
                buildServerTree(client)


    def scheduleEDFServers(self, leaves, uniServer, time, processors):
        uniServer.initializeTasks()
        uniServer.setExecuting(True)

        printTree(uniServer)
        print()
        print("leaves___")
        print()
        printServers(leaves)
        '''
        for i in range(0, time):

            
            for server in singletonServers:
                if(time % server.getDeadline() == 0):
                    queue.append(EDFTask(time + server.getDeadline(), 
                                 server.getDeadline() * server.getRate())))
            
        '''

        return True



 

def printClasses(server):
        
    if(len(server.getClients()) > 0):
        for client in server.getClients():
            printClasses(client)
    print(server)

if __name__ == "__main__":
    #generate 100 task sets with n tasks = 17
    testTaskSet = [(0.5,5), (0.4, 4), (0.4, 6), (0.3, 3), (0.2, 2), (0.1, 1), (0.1,1)]
    nTasks = 17
    minPeriod = 5
    maxPeriod = 100
    periodGranularity = minPeriod
    nSets = 1
    '''
    for i in range(20, 21):
        rate = i/100
        taskRates = genTaskRates(nTasks, rate, nSets)
        taskPeriods = genTaskPeriods(nTasks, nSets, minPeriod, maxPeriod, minPeriod,"logunif")
        taskSet = []
        for ix,rate in enumerate(taskRates[0]):
            taskSet.append((rate, taskPeriods[0][ix]))
        scheduler = RunScheduler()
        servers = scheduler.convertToSingletonServers(taskSet)       
        uniServer, serversC = scheduler.reduceToUniserver(servers)
        #uniServer[0].setExecuting(True)
        uni = uniServer[0]
        uni.setExecuting(True)
        #printTree(uni)
        print()
        print("-----------------")
        print()
        printServers(serversC)
    '''
    scheduler = RunScheduler()
    servers = scheduler.convertToSingletonServers(testTaskSet)
    uniServer, serversC = scheduler.reduceToUniserver(servers)
    printTree(uniServer[0])
    print()
    print("___initial states ____")
    scheduler.scheduleEDFServers(serversC, uniServer[0], 100, 1)
  

##Problem with reduction tree, all of the base servers are the duals not the
##singletons    
    

        

