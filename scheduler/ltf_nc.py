from scheduler.base_scheduler import Scheduler
from operator import attrgetter

# fragmentable
class Longest_Task_First_Scheduler_NC(Scheduler):
    def __init__(self,num_machines, jobs, create_schedule):
        super().__init__(num_machines, jobs, create_schedule)
    
    def schedule(self):
        # sort jobs by execution_time in decreasing order
        self.jobs.sort(reverse=True, key=attrgetter('execution_time'))

        for job in self.jobs:
            # find indices of k (=job.required_machines) machines which will be available first
            threshold = self.find_k_smallest_utilization(job.required_machines)
            available_machine_indices = self.find_machines_with_utilization_at_most(threshold)
            needed_machine_indices = available_machine_indices[0:job.required_machines]

            self.place_job(job, needed_machine_indices, start_execution_time=threshold)
            
        return self.find_makespan()

