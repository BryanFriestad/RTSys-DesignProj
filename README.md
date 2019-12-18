# RTSys-DesignProj
Final design project for Computer Engineering 458/558: Real Time Systems. The project is a simulation study comparing the overhead efficiency of two multiprocessor scheduling algorithms. 
Specifically, we will be comparing the RUN (Reduction to UNiprocessor) and P-Fair algorithms.

# P-Fair Algorithm
### The P-Fair algorithm is contingent upon two things: 
1. The idea of lag, which is defined by: lag(Ti, t) = t*(Ci/Pi) - time_allocated(Ti, t) [4, pg 5]. Where Ti is the i-th task, t is the current time Ci is the computation time of task i 
and Pi is the period of task i. The function time_allocated(Ti, t) returns the amount of time given to all instances of this task from time = [0,  t).
2. Unit execution, meaning tasks are broken down and performed in 1 time unit blocks each until finished.

With the above contingencies understood, the algorithm is fairly simple. The data structures described above should contain all of the information necessary to implement this algorithm. 
It should be noted that if a task is scheduled, its lag decreases by 1 - (Ci/Pi). If a task is not scheduled, its lag is increased by (Ci/Pi). After executing one time unit, adjust the 
lag of Ti by the amount described, depending on whether or not it executed. The algorithm is an online scheduler, as priorities are assigned dynamically. The algorithm [4, pg 12] is as 
follows:

1. Schedule all urgent tasks (assign priority 1) 
   - A task is urgent at time t if:
	 * lag(Ti, t) > 0 and 
	 * lag(Ti, t+1) >= 0 given task Ti executes in the following time unit.
2. Do not execute any “tnegru” tasks (assign priority infinity) 
   - A task is “tnegru” at time t if:
	 * lag(Ti, t) < 0 and
	 * lag(Ti, t+1) <= 0 given task Ti does not execute in the next time unit.
3. For the remaining tasks, execute the ones with minimal t’ > t where lag(Ti, t’) is greater than 0.
