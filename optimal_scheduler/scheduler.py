import itertools
from approximate_scheduler.base_scheduler import Scheduler
from typedefs import Job, Placed_Job, Schedule
from operator import methodcaller


# Very slow. I wouldn't try much more than 5 jobs and m=5
class Optimal_Scheduler:
    def __init__(self, NUM_MACHINES : int, jobs : list[Job], CREATE_SCHEDULE: bool, IS_FRAGMENTABLE : bool):
        self.NUM_MACHINES = NUM_MACHINES
        self.machine_utilization = [0]*self.NUM_MACHINES 
        self.placed_jobs = []
        self.jobs = jobs
        self.CREATE_SCHEDULE = CREATE_SCHEDULE
        self.IS_FRAGMENTABLE = IS_FRAGMENTABLE
        
    def find_makespan(self):
        return max(self.machine_utilization)

    def get_schedule(self):
        return Schedule(self.placed_jobs, self.NUM_MACHINES)
    
    def schedule(self):
        scheduler = self.__schedule(remaining_jobs=self.jobs, shuffled_jobs=[])
        self.machine_utilization = scheduler.machine_utilization
        self.placed_jobs = scheduler.placed_jobs
        return self.find_makespan()

    # produces all possible permutations of the jobs and call then calls __place_jobs
    def __schedule(self, remaining_jobs : list[Job], shuffled_jobs : list[Job]) -> Scheduler:
        # shuffle the list in every possible way
        if len(remaining_jobs) > 0:
            possible_scheduler : list[Scheduler] = []
            for i in range(len(remaining_jobs)):
                shuffled_jobs_copy = list(shuffled_jobs)
                remaining_jobs_copy = list(remaining_jobs)

                shuffled_jobs_copy.append(remaining_jobs_copy[i])
                remaining_jobs_copy.pop(i)

                possible_scheduler.append(self.__schedule(remaining_jobs_copy, shuffled_jobs_copy))

            # return the best try (for every shuffle of jobs) (the scheduler in the list with minimal makespan)
            return min(possible_scheduler, key=methodcaller('find_makespan'))

        # try placing a block at every possible starting location
        else:
            scheduler = Scheduler(self.NUM_MACHINES, jobs=None, CREATE_SCHEDULE=self.CREATE_SCHEDULE)
            return self.__place_jobs(jobs=shuffled_jobs, current_job_index=0, scheduler=scheduler)


    # takes a list of (shuffled) jobs and places them in order at every possible position
    def __place_jobs(self, jobs : list[Job], current_job_index : int, scheduler : Scheduler) -> Scheduler:
        if len(jobs) > current_job_index:
            possible_scheduler : list[Scheduler] = []
            next_job = jobs[current_job_index]

            if self.IS_FRAGMENTABLE:
                # all subsets of [0,1,...,m-1] of size 'required_machines"
                all_possible_job_indices = list(itertools.combinations(range(0,self.NUM_MACHINES), next_job.required_machines))
            else:
                # all contiguous subsets of [0,1,...,m-1] of size 'required_machines"
                all_possible_job_indices = [range(i,i+next_job.required_machines) for i in range(self.NUM_MACHINES-next_job.required_machines+1)]

            # try every possibility to place the next job
            for job_indices in all_possible_job_indices:
                # copy scheduler
                scheduler_copy = Scheduler(self.NUM_MACHINES, jobs=None, CREATE_SCHEDULE=True)
                scheduler_copy.placed_jobs = list(scheduler.placed_jobs)
                scheduler_copy.machine_utilization = list(scheduler.machine_utilization)

                # place next job
                # maximum but only concerning the job_indices
                max_utilization = max([scheduler.machine_utilization[i] for i in job_indices])
                scheduler_copy.place_job(next_job, job_indices, start_execution_time=max_utilization)

                possible_scheduler.append(self.__place_jobs(jobs, current_job_index+1, scheduler_copy))

            # return the best try (for this shuffle of jobs) (the scheduler in the list with minimal makespan)
            return min(possible_scheduler, key=methodcaller('find_makespan'))
        
        else:
            return scheduler
    
