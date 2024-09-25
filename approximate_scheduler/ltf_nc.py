from approximate_scheduler.base_scheduler import Scheduler
from operator import attrgetter

# fragmentable
class LTF_Scheduler(Scheduler):
    def __init__(self,NUM_MACHINES, jobs, CREATE_SCHEDULE):
        super().__init__(NUM_MACHINES, jobs, CREATE_SCHEDULE)
    
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

