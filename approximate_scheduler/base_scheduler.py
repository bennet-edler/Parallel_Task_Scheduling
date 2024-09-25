from typedefs import Job, Schedule, Placed_Job
import random


class Scheduler:
    
    def __init__(self, NUM_MACHINES : int, jobs : list[Job], CREATE_SCHEDULE: bool):
        self.NUM_MACHINES = NUM_MACHINES
        self.machine_utilization = [0]*self.NUM_MACHINES 
        self.placed_jobs = []
        self.jobs = jobs
        self.CREATE_SCHEDULE = CREATE_SCHEDULE
        
    def find_machines_with_utilization_at_most(self, max_utilization):
        indices = []

        # take the first machines which are under the threshold
        for i in range(len(self.machine_utilization)):
            current_utilization = self.machine_utilization[i]
            if current_utilization <= max_utilization:
                indices.append(i)
        return indices

    # find utilization with index k in the ordered list
    def find_k_smallest_utilization(self, k : int): # TODO implement linear algorithm
        utilization_copy = list(self.machine_utilization)
        utilization_copy.sort(reverse = False) 

        return utilization_copy[k-1]

    def find_makespan(self):
        return max(self.machine_utilization)

    def generate_random_jobs(
            number_of_jobs, min_execution_time, max_execution_time,
            min_required_machines, max_required_machines, float_execution_time=False
            ):
        jobs = []
        for _ in range(1,number_of_jobs+1):
            required_machines = random.randint(min_required_machines,max_required_machines)
            execution_time = 0
            if float_execution_time==False:
                execution_time = random.randint(min_execution_time,max_execution_time)
            else:
                execution_time = random.uniform(min_execution_time,max_execution_time)
                if execution_time == min_execution_time:
                    execution_time = max_execution_time
            jobs.append(Job(required_machines, execution_time))
        return jobs

    def get_schedule(self):
        return Schedule(self.placed_jobs, self.NUM_MACHINES)


    def place_job(self, job : Job, indices : list[int], start_execution_time : int):
        # update machine utilization
        for index in indices:
            self.machine_utilization[index] = start_execution_time + job.execution_time

        # remember where jobs are placed. just needed to draw a picture (so can be removed for better performance)
        if self.CREATE_SCHEDULE:
            self.placed_jobs.append(Placed_Job(job, indices, start_execution_time))

