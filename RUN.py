import copy
class Server:
    clients = []

    def getRate(self):
        total = 0
        for client in clients:
            total += client.getRate()
    
    def getDeadline(self):
        latest = 0
        for client in clients:
            if(client.getDeadline() > latest):
                latest = client.getDeadline
        return latest
    
    def isUnitServer(self):
        if(self.getRate() == 1):
            return true
        else
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
def convertToSingletonServers(taskset)
    for task in taskset:
        #task
    
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
            

