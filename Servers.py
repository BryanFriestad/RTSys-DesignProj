import copy
import sys

class ServerEDF:
    clients = []
    rate = -1
    deadline = -1
    executing = False
    
    def __init__(self, clients, rate, deadline):
        
        self.clients = clients
        
        if(rate == None) : self.rate = self.getRate()
        else: self.rate = rate
        
        if(deadline == None): self.deadline = self.getDeadline()
        else: self.deadline = deadline
        
        
    def setExecuting(self, a):
        self.executing = True

    def isExecuting(self): return self.executing

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
