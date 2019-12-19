
class EDFTask:

	executing = False
	deadline = 0
	rCompute = 0
	topCompute = 0
	premptions = 0
	prevTime = 0
	ready = False
	isCompleted = False
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
			self.executing = False
			self.ready = False
			return True

		if(time > deadline):
			return False

		if(time <= deadline):
			return True
	
	def startExecuting(self): 
		self.executing = True
		self.ready = False

	def pause(self): 
		self.executing = False
		self.ready = True
		self.premptions += 1

	def isCompleted(self): return self.completed
	def isReady(self): return self.ready

	def getDeadline(self): return self.deadline
	def setProcessor(self, processor): self.previousProcessorId = processor
	def getPrevProcessor(self): return self.previousProcessorId

	def remake(self):
		self.rCompute = self.topCompute
		self.ready = True


	def __str__(self):
		 return "rCompute: " + str(self.rCompute) + " | Deadline: " + str(self.deadline) + \
                " | Executing: " + str(self.executing) 

class PFairTask:

	readyTime = 0
	period = 0
	deadline = 0
	computeTime = 0
	lag = 0
	allocatedTime = 0
	premptions = 0
	migrations = 0
	isCompleted = False

	def __init__(self, ri, pi, ci):
		'''
		initialized with compute time and period
		'''
		self.readyTime = ri
		self.period = pi
		self.deadline = pi
		self.computeTime = ci

class Processor:

	task = None
	def updateTime(self,time):
		if self.task is not None:
			if(self.task.updateTime(time)):
				if(self.task.isCompleted): 
					self.task = None
			else: return False
		else: return True

	def runTask(self, task):
		self.task = task

	def isFree(self): 
		if(self.task is not None):
			return False
		else:
			return True

	def __str__(self):
		return str(self.task)
