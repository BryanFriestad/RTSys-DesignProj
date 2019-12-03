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
    
    def scheduleTasksEDF(self):
        #TODO
        for client in clients:
            

def convertToSingletonServers(taskset)
    for task in taskset:
        #task