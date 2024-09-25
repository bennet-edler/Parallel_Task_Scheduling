from typedefs import Job, Test_Case, Plot_Data, Instance
import json

class Instance_With_Results:
    def __init__(self, num_machines : int , jobs : dict, results : dict[str]):
        self.num_machines = num_machines
        self.jobs = jobs
        self.results = results
        
def test_schedulers_and_store_results(Schedulers_To_Test : list, num_machines : int, jobs : list[Job], filepath : str) -> None:
    # run all Schedulers in Schedulers_To_Test successively and remember the makespan
    resulting_makespans = {}
    for Next_Scheduler in Schedulers_To_Test:
        scheduler = Next_Scheduler(num_machines, jobs, CREATE_SCHEDULE=False)
        makespan = scheduler.schedule()
        resulting_makespans["Makespan " + type(scheduler).__name__] = makespan

    # store the results in a file
    with open('data.json', 'w') as out_file:
        job_dictionary = [job.__dict__ for job in jobs]
        json.dump(Instance_With_Results(num_machines, jobs=job_dictionary, results=resulting_makespans).__dict__,
                   out_file, sort_keys=True, indent=4)
        
def load_jobs(filepath: str) -> list[Job]:
    jobs = []
    with open(filepath, 'r') as in_file:
        json_jobs = json.load(in_file)['jobs']
        for job in json_jobs:
            jobs.append(Job(required_machines=job['required_machines'], execution_time=job['execution_time']))
    return jobs 


def store_test_cases(filepath: str, test_cases : list[Test_Case]):
    with open(filepath, 'w') as out_file:
        json.dump(test_cases, out_file, sort_keys=True, indent=4, default=vars)

def __extract_instances(instances_dict):
    instances = []
    for instance in instances_dict:
        jobs = []
        jobs_dict = instance['jobs']
        for job in jobs_dict:
            jobs.append(Job(required_machines=job['required_machines'], execution_time=job['execution_time']))
        m = instance['m']
        instances.append(Instance(m,jobs))
    return instances


def load_test_cases(filepath: str) -> list[Test_Case]:
    test_cases = []
    with open(filepath, 'r') as in_file:
        json_data = json.load(in_file)
        for test_case in json_data:
            instances = __extract_instances(test_case['instances'])
            x_value = test_case['x_value']
            test_cases.append(Test_Case(instances, x_value))
    return test_cases



    