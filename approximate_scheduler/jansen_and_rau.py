from typedefs import Placed_Job, Job
from approximate_scheduler.base_scheduler import Scheduler
from operator import attrgetter
from approximate_scheduler.list import LIST_Scheduler
from typedefs import Placed_Job


# fragmentable
class Jansen_And_Rau_Scheduler(Scheduler):
    def __init__(self,NUM_MACHINES, jobs, CREATE_SCHEDULE):
        super().__init__(NUM_MACHINES, jobs, CREATE_SCHEDULE)
    
    def schedule(self):
        # sort jobs by required_machines in decreasing order
        self.jobs.sort(reverse=True, key=attrgetter('required_machines'))
        
        # jobs with m/2 >= required machines > m/3
        big_jobs = []
        # jobs with required machines <= m/3
        small_jobs = []
        for i in range(len(self.jobs)):
            # place jobs with required_machines > m/2
            job = self.jobs[i]
            if job.required_machines > self.NUM_MACHINES/2:
                indices = range(self.NUM_MACHINES-job.required_machines,self.NUM_MACHINES)
                self.place_job(job, indices, start_execution_time=self.machine_utilization[-1])

            elif job.required_machines >= self.NUM_MACHINES/3:
                big_jobs.append(job)
            else:
                small_jobs.append(job)

        # place big_jobs (on list scheduler)
        list_scheduler = LIST_Scheduler(self.NUM_MACHINES,big_jobs,CREATE_SCHEDULE=True)
        list_scheduler.machine_utilization = self.machine_utilization
        list_scheduler.schedule()

        # the point in time, where the last job with required_machines > m/2 ends
        tau_prime = self.machine_utilization[-1]

        # the last point in the schedule where two jobs are processed
        T_prime = 0
        last_job : Placed_Job         = list_scheduler.placed_jobs[-1]
        if len(list_scheduler.placed_jobs) >= 2:
            second_last_job : Placed_Job  = list_scheduler.placed_jobs[-2]

            T_prime = min(last_job.starting_time + last_job.job.execution_time, 
                          second_last_job.starting_time + second_last_job.job.execution_time)
        elif len(self.placed_jobs) == 1:
            T_prime = last_job.starting_time + last_job.job.execution_time

        T = max(T_prime, tau_prime) 
        #print("T: ", T)

        # total processing time, where exactly 2 jobs are scheduled
        b = 0
        for placed_job in list_scheduler.placed_jobs:
            time_finished = placed_job.starting_time + placed_job.job.execution_time 
            isOnLeftSide  = placed_job.machine_indices[0] == 0
            if time_finished <= T and isOnLeftSide:
                b += placed_job.job.execution_time
            # one job might start before T and finished after T so it will be only partially added
            elif placed_job.starting_time < T and isOnLeftSide:
                b += T-placed_job.starting_time

        
        # total processing time before T, where only one job is scheduled
        a = T - b

        if a > b:
            # reset schedule
            self.placed_jobs = []
            self.machine_utilization = [0] * self.NUM_MACHINES

            # place jobs with required_machines > m/3
            for i in range(len(self.jobs)):
                job = self.jobs[i]
                if job.required_machines > self.NUM_MACHINES/3:
                    indices = range(self.NUM_MACHINES-job.required_machines,self.NUM_MACHINES)
                    self.place_job(job, indices, start_execution_time=self.machine_utilization[-1])
        else:
            # place big_jobs (on this scheduler) 
            self.placed_jobs = self.placed_jobs + list_scheduler.placed_jobs
            self.machine_utilization = list_scheduler.machine_utilization

        # place all remaining jobs (small_jobs)
        list_scheduler = LIST_Scheduler(self.NUM_MACHINES,small_jobs,CREATE_SCHEDULE=self.CREATE_SCHEDULE)
        list_scheduler.machine_utilization = self.machine_utilization
        list_scheduler.schedule()

        self.machine_utilization = list_scheduler.machine_utilization
        self.placed_jobs = self.placed_jobs + list_scheduler.placed_jobs
        
        return self.find_makespan()