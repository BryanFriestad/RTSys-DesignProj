
class EDFTask:

	executing = False
	deadline = 0
	rCompute = 0
	premptions = 0
	prevTime = 0
	isCompleted = False

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
		if(self.isExecuting()):
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
