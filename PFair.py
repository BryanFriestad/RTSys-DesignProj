from __future__ import division
from Task import PFairTask as PFairTask
import taskgen
import numpy
import random

def countPreemptions(schedule):
    count = 0
    for x in range(1, len(schedule)):
        for y in range(len(schedule[x])):
            if(schedule[x][y] != schedule[x-1][y]):
                if(schedule[x-1][y] is not None):
                    count += 1
    return count

class PFScheduler:
    
    def __init__(self, processorCount):
        self.numProc = processorCount
        self.tasks = []
        self.time = 0
        self.schedule = []
        self.num_jobs = 0

    def generateSchedule(self, taskset, runTime):
        self.initTaskInstances(taskset, runTime)
        for x in range(runTime):
            self.scheduleFrame()
        return self.schedule

    def initTaskInstances(self, taskset, runTime):
        #each task will have a unique ID
        iden = 0
        #for each task in the taskset
        i = 0
        for task in taskset:
            i += 1
            j = 0
            period = task[1] #get the period
            #for each instance up until the end of the runTime
            for ri in range(0, runTime, period):
                j += 1
                self.tasks.append(PFairTask(ri, task[0], period, iden, i, j)) #add an instance to the task list
                iden += 1
        #print("Task set: " + str(self.tasks))
        self.num_jobs = len(self.tasks)
        print("Total number of jobs: " + str(len(self.tasks)))

    def scheduleFrame(self):
        urgent_tasks = []
        tnegru_tasks = []
        safe_tasks = []
        
        for task in self.tasks:
            if(task.readyTime <= self.time):
                if(task.isUrgent()):
                    urgent_tasks.append(task) #find all urgent tasks
                elif(task.isTnegru()):
                    tnegru_tasks.append(task) #find all tnegru tasks
                else:
                    safe_tasks.append(task) #all of the remaining tasks

        #print("Urgent tasks: " + str(urgent_tasks))
        #print("Tnegru tasks: " + str(tnegru_tasks))
        #print("Safe tasks: " + str(safe_tasks))

        #for this frame, all processors are unallocated at this point
        remaining_processor_slots = self.numProc
        scheduled_tasks = []

        #schedule all urgent tasks
        if(len(urgent_tasks) > remaining_processor_slots):
            print("Error: too many urgent tasks")
        scheduled_tasks = list(urgent_tasks)
        remaining_processor_slots -= len(urgent_tasks)
        
        #do not schedule any tnegru tasks
        
        #from the safe tasks list, do the following
        i = 0
        while(remaining_processor_slots > 0):
            if(len([t for t in safe_tasks if t not in scheduled_tasks]) == 0):
                break; #this means all safe tasks have been scheduled already
            tied_tasks = []
            for t in safe_tasks:
                #print("future lag of " + str(t) + ": " + str(t.futureLag(i)))
                if(t.futureLag(i) > 0):
                    tied_tasks.append(t) #gets all tasks which will have positive lag at time+i
            #print("Tied tasks" + str(tied_tasks))
            tied_tasks = [t for t in tied_tasks if t not in scheduled_tasks] #removes ones already scheduled
            while(len(tied_tasks) > remaining_processor_slots):
                #remove the tied task with smallest lag at time
                smallest_lag = tied_tasks[0].futureLag(i)
                smallest_lag_task = tied_tasks[0]
                for x in range(1, len(tied_tasks)):
                    if(tied_tasks[x].futureLag(i) < smallest_lag):
                        smallest_lag = tied_tasks[x].futureLag(i)
                        smallest_lag_task = tied_tasks[x]
                tied_tasks.remove(smallest_lag_task)
            for t in tied_tasks:
                scheduled_tasks.append(t) #add remaining tasks to the scheduled task list
            remaining_processor_slots -= len(tied_tasks) #remove available processors
            i += 1

        for x in range(remaining_processor_slots):
            scheduled_tasks.append(None)
            
        #print("Scheduled tasks" + str(scheduled_tasks))

        #TODO: after determining the tasks to be scheduled, assign them to reduce preemptions
        self.schedule.append(scheduled_tasks)
        
        for t in scheduled_tasks:
            if(t is not None):
                t.remainingCompute -= 1 #reduce 1 from remainingCompute of all executed tasks

        #updates lag of all tasks
        for t in urgent_tasks:
            t.updateLag(True)
        for t in tnegru_tasks:
            t.updateLag(False)
        for t in safe_tasks:
            if(t in scheduled_tasks):
                t.updateLag(True)
            else:
                t.updateLag(False)

        #remove all completed tasks from the readyTasks list
        incomplete_tasks = []
        for t in self.tasks:
            if(t.remainingCompute > 0):
                incomplete_tasks.append(t)
        self.tasks = list(incomplete_tasks)
            
        self.time += 1
        #print 
        
if __name__ == "__main__":
    avg = 0
    tasks = 0
    reps = 25
    for r in range(reps):
        task_set = []
        runtime = 1000
        processors = 4
        utilization = 0.1
        num_tasks = 32
        min_period = 5
        max_period = 100

        x = taskgen.StaffordRandFixedSum(num_tasks, utilization * processors, 1)
        periods = taskgen.gen_periods(num_tasks, 1, min_period, max_period, min_period, "unif")
        #iterate through each row (which represents utils for a taskset)
        for i in range(numpy.size(x, axis=0)):
            C = x[i] * periods[i]
            C = numpy.trunc(C)
            for j in range(len(C)):
                task = [int(C[j]), int(periods[i][j])]
                task_set.append(task)

        final_taskset = []
        for t in task_set:
            if(t[0] != 0):
                final_taskset.append(t)
        tasks += len(final_taskset)
        print(final_taskset)
        scheduler = PFScheduler(processors)
        end_sched = scheduler.generateSchedule(final_taskset, runtime)
        '''
        for x in range(processors):
            for frame in end_sched:
                print(frame[x]),
            print
        '''
        preemp_count = countPreemptions(end_sched)
        instance_count = scheduler.num_jobs
        print("Preemptions/Instance: " + str(preemp_count/instance_count))
        avg += preemp_count/instance_count
        print
    avg = avg / reps
    print("average = " + str(avg))
    print("total tasks = " + str(tasks))

        
    
