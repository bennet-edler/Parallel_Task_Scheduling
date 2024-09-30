from typedefs import Test_Case, Plot_Data
from approximate_scheduler.base_scheduler import Scheduler
from approximate_scheduler.ltf_nc import LTF_Scheduler
from approximate_scheduler.ltf_c import Shelf_Scheduler
from approximate_scheduler.list import List_Scheduler
from approximate_scheduler.jansen_and_rau import JR_Scheduler
from approximate_scheduler.tower import Tower_Scheduler
from optimal_scheduler.not_fragmentable import Not_Fragmentable_Scheduler
from optimal_scheduler.fragmentable import Fragmentable_Scheduler
from statistics import mean

# execute a list of schedulers on a list of test cases
# and fill Plot_Data for every scheduler 
class Analyzer:
    def __init__(self, Schedulers_To_Test, test_cases : list[Test_Case]):
        self.Schedulers_To_test = Schedulers_To_Test
        self.test_cases : list[Test_Case] = test_cases
        self.max_list_makespans = []

    def __execute_instances(max_list_makespans, test_case, Scheduler, normalized : bool):
        makespans = []
        normalized_makespans = []
        # exectute every instance
        for instance in test_case.instances:
            scheduler = Scheduler(instance.m, instance.jobs, CREATE_SCHEDULE=False)
            makespan = scheduler.schedule()
            makespans.append(makespan)

            # normalize the makespan and append
            if normalized:
                normalized_makespans.append(makespan/instance.lower_bound)
        
        # save worst list makespan for every test_case (will be used as an upper bound for the ratio)
        if Scheduler == List_Scheduler:
            max_makespan = max(makespans)
            max_list_makespans.append(max_makespan)
        if normalized:
            return normalized_makespans
        return makespans

    # for 'calculate_ratios' to work must one Scheduler be LIST_Scheduler
    def analyze_schedulers(Schedulers_To_Test, test_cases : list[Test_Case], normalized : bool):
        max_list_makespans = []
        plot_data_list : list[Plot_Data] = []

        # test every scheduler
        for Scheduler in Schedulers_To_Test:
            plot_data = Plot_Data()
            print("finished test cases:")

            # execute every test case
            for j in range(len(test_cases)):
                test_case = test_cases[j]
                makespans = Analyzer.__execute_instances(max_list_makespans, test_case, Scheduler, normalized)

                # store means and deviations
                mean_value = round(mean(makespans),5)
                plot_data.means.append(mean_value)
                plot_data.neg_deviations.append(mean_value - min(makespans))
                plot_data.pos_deviations.append(max(makespans) - mean_value)

                plot_data.scheduler_name = Scheduler.__name__
                print("    " + str(j) + ", mean=" + str(mean_value))
            plot_data_list.append(plot_data)
        return plot_data_list
