from typedefs import Placed_Job, Job
from approximate_scheduler.base_scheduler import Scheduler
from operator import attrgetter



# fragmentable
class LIST_Scheduler(Scheduler):
    def __init__(self,NUM_MACHINES, jobs, CREATE_SCHEDULE):
        super().__init__(NUM_MACHINES, jobs, CREATE_SCHEDULE)
    
    def schedule(self):
        # sort jobs by required_machines in decreasing order
        self.jobs.sort(reverse=True, key=attrgetter('required_machines'))

        jobs_copy = list(self.jobs)
        
        for _ in range(len(self.jobs)):
            # find gap where the smallest job fits in
            smallest_required_machines = jobs_copy[-1].required_machines
            threshold = self.find_k_smallest_utilization(smallest_required_machines) 
            available_machine_indices = self.find_machines_with_utilization_at_most(threshold)
            gap_size = len(available_machine_indices)

            # place biggest fitting job in the gap
            for j in range(len(jobs_copy)): # TODO: binary search
                job = jobs_copy[j]
                if job.required_machines <= gap_size:
                    needed_indices = available_machine_indices[0:job.required_machines]
                    self.place_job(job, needed_indices, start_execution_time=threshold)
                    jobs_copy.pop(j)
                    break

        return self.find_makespan()
            

