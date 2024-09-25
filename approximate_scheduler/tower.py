from typedefs import Placed_Job, Job
from approximate_scheduler.base_scheduler import Scheduler
from approximate_scheduler.list import List_Scheduler
from operator import attrgetter
from math import floor

# intervals are here open on the left and closed on the right
class Interval:
    def __init__(self,left, right):
        self.left = left
        self.right = right

    def contains(self, number):
        if number > self.left and number <= self.right:
            return True
        return False

# the starting time is missing here. mostly used for jobs which will be moved up.
class Machine_Assignment:
    def __init__(self, job : Job, machine_indices : list[int]):
        self.job = job
        self.machine_indices = machine_indices


# fragmentable
class Tower_Scheduler(Scheduler):
    def __init__(self,NUM_MACHINES, jobs, CREATE_SCHEDULE):
        super().__init__(NUM_MACHINES, jobs, CREATE_SCHEDULE)

    def schedule(self):
        self.jobs.sort(reverse=True, key=attrgetter('required_machines'))
        self.list(interval=Interval(3/4,1))

        self.tower_algorithm(tower_interval=Interval(1/2,3/4), fill_interval=Interval(1/4,1/2))
        self.tower_algorithm(tower_interval=Interval(1/3,3/8), fill_interval=Interval(1/4,1/3))

        self.list(Interval(3/8,1/2))
        self.list(Interval(1/4,1/3))
        self.list(Interval(0,1/3))

        return self.find_makespan()

    def tower_algorithm(self, tower_interval : Interval, fill_interval : Interval):
        tower_height : int             = self.place_tower(tower_interval)

        # find jobs which will be later moved up
        fill_jobs : list[Machine_Assignment] = self.find_fitting_jobs(interval=fill_interval, height=tower_height)
        
        # calculate how much space the fill_jobs leave and find fitting smaller jobs
        fill_height : int = self.find_fill_height(fill_jobs)
        scheduling_height = tower_height-fill_height
        small_interval = Interval(0,fill_interval.left)
        small_jobs : list[Machine_Assignment] = self.find_fitting_jobs(interval=small_interval, height=scheduling_height)

        # schedule first the small_jobs and then the fill_jobs on top
        self.place_machine_assignments(small_jobs)
        self.place_machine_assignments(fill_jobs)

    # place jobs in 'tower_interval'. if multiple are fitting next to each other,
    # let the next one begin where the last one ends in the worst case
    def place_tower(self, tower_interval: Interval):
        # find placing locations for the jobs with machine requirement in tower_interval
        placing_locations = [self.NUM_MACHINES-1]
        location = self.NUM_MACHINES-1 - tower_interval.right * self.NUM_MACHINES
        while(location >= tower_interval.right * self.NUM_MACHINES):
            placing_locations.append(floor(location))
            location -= tower_interval.right * self.NUM_MACHINES

        # place jobs with machine requirement in tower_interval 
        tower_jobs = self.filter(tower_interval)
        for j in range(len(tower_jobs)):
            job : Job = tower_jobs[j]
            # place them on the machine with least machine utilization which is in placing_locations
            placing_location = min(placing_locations, key=lambda location: self.machine_utilization[location])
            machine_indices  = range(placing_location-job.required_machines+1, placing_location+1)
            starting_time    = self.machine_utilization[placing_location]
            self.place_job(job, machine_indices, starting_time)
                
        # no job shall be active after this time
        tower_height = max(self.machine_utilization)

        return tower_height

    # find jobs with machine requirement in 'interval' and with scheduled height no more than 'height'
    def find_fitting_jobs(self, interval : Interval, height : int):
        job_candidates = self.filter(interval)

        # try to schedule all jobs in the interval
        list_scheduler = List_Scheduler(self.NUM_MACHINES, job_candidates, CREATE_SCHEDULE=True)
        list_scheduler.machine_utilization = list(self.machine_utilization)
        list_scheduler.schedule()
        
        # return those which do not violate the height constraint
        jobs = []
        placed_job : Placed_Job
        for placed_job in list_scheduler.placed_jobs:
            job = placed_job.job
            ending_time = placed_job.starting_time + job.execution_time
            if ending_time <= height:
                jobs.append(Machine_Assignment(job, placed_job.machine_indices))
            else:
                self.jobs.append(job)

        self.jobs.sort(reverse=True, key=attrgetter('required_machines'))
        return jobs
    
    # schedules fill_jobs on empty schedule and returns the makespan
    def find_fill_height(self,fill_jobs):
        machine_utilization = [0]*self.NUM_MACHINES
        machine_assignment : Machine_Assignment
        for machine_assignment in fill_jobs:
            job = machine_assignment.job

            for index in machine_assignment.machine_indices:
                machine_utilization[index] += job.execution_time

        return max(machine_utilization)
    
    # places the given machine_assignments on the schedule
    def place_machine_assignments(self, machine_assignments : list[Machine_Assignment]):
        for machine_assignment in machine_assignments:
            job             = machine_assignment.job
            machine_indices = machine_assignment.machine_indices
            starting_time   = max([self.machine_utilization[i] for i in machine_indices])
            self.place_job(job, machine_indices, starting_time)

    # remove jobs which are in 'interval' and return them
    def filter(self, interval : Interval):
        jobs_copy = list(self.jobs)
        self.jobs = []

        jobs = []
        for j in range(len(jobs_copy)):
            job = jobs_copy[j]
            if interval.contains(job.required_machines/self.NUM_MACHINES):
                jobs.append(job)
            else:
                self.jobs.append(job)
        
        return jobs
 
    # list-schedule jobs in 'interval'
    def list(self, interval : Interval):
        jobs = self.filter(interval)
        list_scheduler = List_Scheduler(self.NUM_MACHINES, jobs, CREATE_SCHEDULE=self.CREATE_SCHEDULE)
        list_scheduler.machine_utilization = list(self.machine_utilization)
        list_scheduler.schedule(aligned_right=True)
        self.placed_jobs = self.placed_jobs + list_scheduler.placed_jobs
        self.machine_utilization = list_scheduler.machine_utilization   


            
