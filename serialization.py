from typedefs import Job
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