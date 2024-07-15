from approximate_scheduler.base_scheduler import Scheduler
from approximate_scheduler.ltf_nc import Longest_Task_First_Scheduler_NC
from approximate_scheduler.ltf_c import Longest_Task_First_Scheduler_C
from approximate_scheduler.list import LIST_Scheduler
from approximate_scheduler.jansen_and_rau import Jansen_And_Rau_Scheduler
from approximate_scheduler.tower import Tower_Scheduler
from optimal_scheduler.not_fragmentable import Not_Fragmentable_Scheduler
from optimal_scheduler.fragmentable import Fragmentable_Scheduler
from visualization import visualize_scheduler
from serialization import test_schedulers_and_store_results, load_jobs
from typedefs import Job

if __name__ == "__main__":
    # generate random jobs
    jobs = Scheduler.generate_random_jobs(
            number_of_jobs=50, min_execution_time=1, max_execution_time=10,
            min_required_machines=1, max_required_machines=399)
    
    jobs += Scheduler.generate_random_jobs(
            number_of_jobs=25, min_execution_time=1, max_execution_time=40,
            min_required_machines=1, max_required_machines=200)
    m = 400

    Schedulers_To_Test = [
        LIST_Scheduler,
        Longest_Task_First_Scheduler_NC,
        Longest_Task_First_Scheduler_C,
        Jansen_And_Rau_Scheduler,
        Tower_Scheduler,
        # Not_Fragmentable_Scheduler, 
        # Fragmentable_Scheduler
        ]
    # jobs = load_jobs('data.json')

    test_schedulers_and_store_results(Schedulers_To_Test, num_machines=m, jobs=jobs, filepath="data.json")

    visualize_scheduler(Tower_Scheduler, num_machines=m, jobs=jobs)


 