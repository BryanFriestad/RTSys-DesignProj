import Task

class PFScheduler:
    self.tasks = []
    self.readyTasks = []
    self.numProc = 0
    self.time = 0
    self.schedule

    def __init__(self, processorCount):
        self.numProc = processorCount

    def generateSchedule(self, taskset, runTime):
        initTaskInstances(taskset, runTime)
        for x in range runTime:
            scheduleFrame()
        return self.schedule

    def initTaskInstances(self, taskset, runTime):
        #for each task in taskset
            #create all periodic instances up until runTime
            #add those instances to self.tasks

    def scheduleFrame(self):
        #add all newly ready tasks to the readyTasks list
        
        #find all urgent tasks
        urgent_tasks = []
        #find all tnegru tasks
        tnegru_tasks = []
        #all of the remaining tasks
        safe_tasks = []

        #for this frame, all processors are unallocated at this point
        remaining_processor_slots = self.numProc

        #schedule all urgent tasks
        #do not schedule any tnegru tasks
        #from the safe tasks list, do the following
        '''
        find those tasks which will have the least t'
        where lag(t') > 0
        if there is a tie between two or more processors,
        choose the ones with the highest lag at t'
        do this until all slots are filled
        '''

        #after determining the tasks to be scheduled, assign them to reduce preemptions
        self.time++
        
        
