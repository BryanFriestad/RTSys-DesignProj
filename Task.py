
class EDFTask:

	self.executing = False
	self.deadline = 0
	self.rCompute = 0
	self.premptions = 0
	self.prevTime = 0
	self.isCompleted = False

	def __init__(self, deadline, rCompute):
		'''
		initialized with compute time and absolute deadline
		'''
		self.deadline = deadline
		self.rCompute = rCompute
		self.executing = True

	def isExecuting(self): return self.executing

	def updateTime(self, time):
		'''
		expects absolute time
		'''
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
