from typedefs import Job, Test_Case, Plot_Data, Instance
import json

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



    