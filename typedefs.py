class Job:
    def __init__(self, required_machines : int, execution_time : float):
        self.required_machines = required_machines
        self.execution_time = execution_time

class Placed_Job:
    def __init__(self, job : Job, machine_indices : list[int], starting_time):
        self.job = job
        self.machine_indices = machine_indices
        self.starting_time = starting_time


class Schedule:
    def __init__(self, placed_jobs : list[Placed_Job], num_machines : int):
        self.placed_jobs  = placed_jobs
        self.num_machines = num_machines

class Instance:
    def __init__(self,m,jobs):
        self.m=m
        self.p_max=max([p_j.execution_time for p_j in jobs])
        self.jobs=jobs

        # upper and lower bound for the optimal value
        volume = 0
        for job in jobs:
            volume += job.required_machines*job.execution_time
        self.lower_bound = volume/m

        self.upper_bound = 0
        for job in jobs:
            self.upper_bound += job.execution_time

class Test_Case:
    def __init__(self,instances, x_value):
        self.x_value = x_value
        self.instances=instances
        self.min_lower_bound = min([instance.lower_bound for instance in self.instances])
        self.max_upper_bound = max([instance.upper_bound for instance in self.instances])
        self.p_max = max([instance.p_max for instance in self.instances])

class Plot_Data:
    def __init__(self):
        self.scheduler_name = ""

        # scheduler makespan
        self.means = []
        self.neg_deviations = []
        self.pos_deviations = []
