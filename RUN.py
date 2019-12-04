import copy
class ServerEDF:
    clients = []
    rate = -1
    deadline = -1
    
    def __init__(self, rate, deadline):
        self.rate = rate
        self.deadline = deadline
    
    def __init__(self, clients, rate, deadline):
        self.rate = rate
        self.deadline = deadline
        self.clients = clients
    def __init__(self, clients):
        self.rate = -1
        self.clients = clients
        
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
        if(self.rate == -1):
            latest = 0
            for client in self.clients:
                if(client.getDeadline() > latest):
                    latest = client.getDeadline
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

class ServerDual:
        
    def __init__(self, edfServer):
        self.rate = 1 - edfServer.getRate()
        self.deadline = edfServer.getDeadline()
        self.edfServer = edfServer
    
    def getRate(self):
        return self.rate
        
    def convertToEDFServer(self):
        return ServerEDF(self.edfServer.getClients(), self.rate, self.deadline)

class runScheduler:
    def pack(self,duals):
        bins = []
        binSpaces = []
        
        for dual in duals:
            index = getEmptiestBinIndex(binSpaces)
            if(binSpaces[index] < dual.getRate()):
                bins.append([dual])
                binSpaces.append(1-dual.getRate())
            else:
                bins[index].append(dual)
        servers = []
        for bin in bins:
            serverSet = []
            for dual in bin:
                serverSet.append(dual.convertToEDFServer())           
            servers.append(ServerEDF(serverSet))
        return servers     
            
    def dual(self, servers):
        duals = []
        for server in servers:
            duals.append(ServerDual(server))
        return duals
    def getEmptiestBinIndex(self,binSpaces):
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
            singleton = ServerEDF(task[0], task[1])
            servers.append(ServerEDF)
        return servers
        
    def reduceToUniserver(self, servers):
        while(len(servers) > 1):
            servers = dual(servers)
            servers = pack(servers)
 
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
            

