from optimal_scheduler.scheduler import Optimal_Scheduler

class Not_Fragmentable_Scheduler(Optimal_Scheduler):
    def __init__(self,num_machines, jobs, CREATE_SCHEDULE):
        super().__init__(num_machines, jobs, CREATE_SCHEDULE, IS_FRAGMENTABLE=False)

        
