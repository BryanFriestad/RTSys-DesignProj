from __future__ import division

class EDFTask:
    executing = False
    deadline = 0
    rCompute = 0
    released = False
    topCompute = 0
    premptions = 0
    prevTime = 0
    ready = False
    completed = False
    previousProcessorId = None

    def __init__(self, deadline, rCompute):
        '''
        initialized with compute time and absolute deadline
        '''
        self.deadline = deadline
        self.rCompute = rCompute
        self.executing = False
        self.ready = True
        self.topCompute = rCompute

    def isExecuting(self): return self.executing

    def updateTime(self, time):
        '''
        expects absolute time
        '''
        if(self.isExecuting()):
            self.rCompute = self.rCompute - (time-self.prevTime)
        self.prevTime = time

        if(self.rCompute == 0): 
            self.completed = True
            self.released = True
            self.executing = False
            self.ready = False
            return True

        if(time > self.deadline):
            return False

        if(time <= self.deadline):
            return True
    
    def startExecuting(self): 
        self.executing = True
        self.ready = False

    def pause(self): 
        self.executing = False
        self.ready = True
        self.premptions += 1

    def isCompleted(self): return self.completed
    def wasReleased(self): return self.released
    def clearReleaseFlag(self): self.released = False
    def isReady(self): return self.ready

    def getDeadline(self): return self.deadline
    def setProcessor(self, processor): self.previousProcessorId = processor
    def getPrevProcessor(self): return self.previousProcessorId

    def remake(self):
        self.rCompute = self.topCompute
        self.ready = True


    def __str__(self):
         return "rCompute: " +  "%0.2f" %self.rCompute + " | Deadline: " + str(self.deadline) + \
                " | Executing: " + str(self.executing) + "| Ready: " + str(self.ready)

class PFairTask:
    def __init__(self, ri, ci, pi, iden, task, inst):
            self.readyTime = ri
            self.period = pi
            self.deadline = pi
            self.computeTime = ci
            self.remainingCompute = ci
            self.id = iden
            self.lag = 0
            self.task_num = task
            self.inst_num = inst

    def __repr__(self):
            return "Task %s->instance %s" % (self.task_num, self.inst_num)

    def __str__(self):
            return "Task %s->instance %s" % (self.task_num, self.inst_num)

    #updates the lag of this task depending on whether or not it executed
    def updateLag(self, wasExecuted):
            if(wasExecuted):
                    self.lag -= (1.0 - (self.computeTime / self.period))
            else:
                    self.lag += (self.computeTime / self.period)
                  
    #returns the lag t time units in the future if this task does not execute
    def futureLag(self, t):
            return self.lag + t*(self.computeTime / self.period)

    #returns whether or not the task is urgent
    def isUrgent(self):
            return (self.lag > 0.0) & (self.lag - (1.0 - (self.computeTime / self.period)) >= 0.0)

    #returns whether or not the task is tnegru
    def isTnegru(self):
            return (self.lag < 0.0) & (self.lag + (self.computeTime / self.period) <= 0.0)

    #returns the lag t time units in the future if this task does not execute
    def futureLag(self, t):
            return lag + t*(self.computetime / self.period)
          
class Processor:

    task = None
    def updateTime(self,time):
        if self.task is not None:
            if(self.task.updateTime(time)):
                if(self.task.isCompleted()): 
                    self.task = None
            else: return False
        else: return True

    def runTask(self, task):
        self.task = task
        task.startExecuting()

    def isFree(self): 
        if(self.task is not None):
            return False
        else:
            return True

    def __str__(self):
        return str(self.task) 
                        