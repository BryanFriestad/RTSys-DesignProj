import copy
from taskgen import StaffordRandFixedSum as genTaskRates
from taskgen import gen_periods as genTaskPeriods
import sys
class ServerEDF:
    clients = []
    rate = -1
    deadline = -1
    
    def __init__(self, clients, rate, deadline):
        
        self.clients = clients
        
        if(rate == None) : self.rate = self.getRate()
        else: self.rate = rate
        
        if(deadline == None): self.deadline = self.getDeadline()
        else: self.deadline = deadline
        
        
        
    def getClients(self): 
        return self.clients
    
    def getRate(self):
        if(self.rate == -1):
            total = 0
            for client in self.clients:
                total += client.getRate()
            return total
        else: return self.rate
    
    def getDeadline(self):
        if(self.deadline == -1):
            latest = 0
            for client in self.clients:
                if(client.getDeadline() > latest):
                    latest = client.getDeadline()
            return latest
        else: return self.deadline
    
    def getComputeTime(self):
        if(self.rate == -1):
            total = 0
            for client in self.clients:
                total += client.getComputeTime()
            return total
        else:
            return self.getRate() * self.getDeadline()
    
    def isUnitServer(self):
        if(self.getRate() == 1):
            return true
        else:
            return false
    
    def scheduleClientsEDF(self):
        #TODO
        queue = []
        totalComputeTime = 0
        sorted = sortClientsByDeadline() 
        for client in sorted:
            if (totalComputeTime + client.getCompute()) > client.getDeadline:
                return False
            else:   
                queue.append(client)
                totalComputeTime += client.getCompute()
        return True
    
    def sortClientsByDeadline(self):
        toSort = copy.deepcopy(self.clients)
        quickSort(toSort, 0, len(toSort)-1)
        return toSort
    def __str__(self):
        return "Rate: " + str(self.rate) + " | Deadline: " + str(self.deadline)
class ServerDual:
        
    def __init__(self, edfServer):
        self.rate = 1 - edfServer.getRate()
        self.deadline = edfServer.getDeadline()
        self.edfServer = edfServer
    
    def getRate(self):
        return self.rate
        
    def convertToEDFServer(self):
        return ServerEDF(self.edfServer.getClients(), self.rate, self.deadline)
     
    def __str__(self):
        return "Rate: " + str(self.rate) + " | Deadline: " + str(self.deadline)

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

 
'''
The following two functions were authored on GeeksforGeeks
   https://www.geeksforgeeks.org/python-program-for-quicksort/
   and modified to fit correct comparision
'''
def partition(arr,low,high): 
    i = ( low-1 )         # index of smaller element 
    pivot = arr[high]     # pivot 
  
    for j in range(low , high): 
  
        # If current element is smaller than or 
        # equal to pivot 
        if   arr[j].getDeadline() <= pivot.getDeadline(): 
          
            # increment index of smaller element 
            i = i+1 
            arr[i],arr[j] = arr[j],arr[i] 
  
    arr[i+1],arr[high] = arr[high],arr[i+1] 
    return ( i+1 ) 
  
# The main function that implements QuickSort 
# arr[] --> Array to be sorted, 
# low  --> Starting index, 
# high  --> Ending index 
  
# Function to do Quick sort 
def quickSort(arr,low,high): 
    if low < high: 
  
        # pi is partitioning index, arr[p] is now 
        # at right place 
        pi = partition(arr,low,high) 
  
        # Separately sort elements before 
        # partition and after partition 
        quickSort(arr, low, pi-1) 
        quickSort(arr, pi+1, high)            
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
            
    
    

        

