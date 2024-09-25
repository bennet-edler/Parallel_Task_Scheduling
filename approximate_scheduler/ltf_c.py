from typedefs import Placed_Job
from approximate_scheduler.base_scheduler import Scheduler
from operator import attrgetter

# not fragmentable
class Shelf_Scheduler(Scheduler):
    def __init__(self, NUM_MACHINES, jobs, CREATE_SCHEDULE):
        super().__init__(NUM_MACHINES, jobs, CREATE_SCHEDULE)
    
    def schedule(self):
        # sort jobs by execution_time in decreasing order
        self.jobs.sort(reverse=True, key=attrgetter('execution_time'))

        shelf_height = 0
        next_shelf_height = self.jobs[0].execution_time
        for job in self.jobs:
            # find indices of k (=job.required_machines) machines which will be available first
            threshold = self.find_k_smallest_utilization(job.required_machines)
            needed_machine_indices = []

            if threshold > shelf_height:
                # update shelf height
                shelf_height = next_shelf_height
                next_shelf_height = shelf_height+job.execution_time

                # use first machines in new shelf
                needed_machine_indices = list(range(0,job.required_machines))
                self.machine_utilization = [shelf_height]*self.NUM_MACHINES
            else:
                # use next machines in old shelf
                available_machine_indices = self.find_machines_with_utilization_at_most(threshold)
                needed_machine_indices = available_machine_indices[0:job.required_machines]

            self.place_job(job, needed_machine_indices, start_execution_time=shelf_height)
        
        return self.find_makespan()