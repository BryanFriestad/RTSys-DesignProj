from __future__ import division
'''
class EDFTask:
	self.executing = False
	self.deadline = 0
	self.rCompute = 0
	self.premptions = 0
	self.prevTime = 0
	self.isCompleted = False

	def __init__(self, deadline, rCompute):
		#initialized with compute time and absolute deadline
		self.deadline = deadline
		self.rCompute = rCompute
		self.executing = True

	def isExecuting(self): return self.executing

	def updateTime(self, time):
		#expects absolute time
		if(isExecuting()):
			self.rCompute = self.rCompute - (time-self.prevTime)
		self.prevTime = time

		if(self.rCompute == 0): 
			self.completed = True
			self.executing = False
			return True

		if(time > deadline):
			return False

		if(time <= deadline):
			return True
	
	def startExecuting(self): self.executing = True

	def pause(self): 
		self.executing = False
		self.premptions += 1

	def isCompleted(self): return self.completed
'''

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
                return "Task %s->instance %s->lag = %s" % (self.task_num, self.inst_num, self.lag)

        def __str__(self):
                return "Task %s->instance %s->lag = %s" % (self.task_num, self.inst_num, self.lag)

        #updates the lag of this task depending on whether or not it executed
	def updateLag(self, wasExecuted):
                if(wasExecuted):
                        self.lag -= (1.0 - (self.computeTime / self.period))
                        print("Here!")
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
                        

