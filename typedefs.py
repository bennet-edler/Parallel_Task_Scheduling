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
