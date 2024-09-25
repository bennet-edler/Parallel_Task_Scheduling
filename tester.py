from typedefs import Test_Case, Instance
from approximate_scheduler.base_scheduler import Scheduler

class Tester:
    def __init__(self,m,n,p_min,p_max,q_min,q_max):
        self.m = m
        self.n = n
        self.p_min = p_min
        self.p_max = p_max
        self.q_min = q_min
        self.q_max = q_max 
        self.test_cases = []

    def generate_one_test_case(self, number_of_instances_per_test_case, float_execution_time : bool, x_value):
        instances = []
        for _ in range(number_of_instances_per_test_case):
            jobs = Scheduler.generate_random_jobs(number_of_jobs=self.n,min_execution_time=self.p_min,max_execution_time=self.p_max,
                                                min_required_machines=self.q_min,max_required_machines=self.q_max, float_execution_time=float_execution_time)
            instance = Instance(self.m,jobs)
            instances.append(instance)
        test_case = Test_Case(instances, x_value)
        self.test_cases.append(test_case)
    
    def get_test_cases(self):
        return self.test_cases