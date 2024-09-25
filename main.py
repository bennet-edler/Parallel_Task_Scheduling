from approximate_scheduler.base_scheduler import Scheduler
from approximate_scheduler.ltf_nc import LTF_Scheduler
from approximate_scheduler.ltf_c import Shelf_Scheduler
from approximate_scheduler.list import List_Scheduler
from approximate_scheduler.jansen_and_rau import JR_Scheduler
from approximate_scheduler.tower import Tower_Scheduler
from optimal_scheduler.not_fragmentable import Not_Fragmentable_Scheduler
from optimal_scheduler.fragmentable import Fragmentable_Scheduler
from visualization import visualize_scheduler
from serialization import test_schedulers_and_store_results, load_jobs, store_test_cases, load_test_cases
from typedefs import Job

from analyzer import Analyzer
from tester import Tester
from plotter import Plotter
import math

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

if __name__ == "__main__":
    Schedulers_To_Test = [
        List_Scheduler,
        LTF_Scheduler,
        Shelf_Scheduler,
        JR_Scheduler,
        Tower_Scheduler,
        # Not_Fragmentable_Scheduler, 
        # Fragmentable_Scheduler
        ]

    # generate random jobs
    number_of_instances_per_test_case=100
    number_of_test_cases=16
    m=200

    # -------- Generate Figure ---------- #
    # code to generate and store the test cases
    """tester = Tester(m=m,n=10,p_min=0,p_max=1,q_min=1,q_max=m)
    for _ in range(number_of_test_cases):
        tester.generate_one_test_case(number_of_instances_per_test_case, float_execution_time=True, x_value=tester.n)
        tester.n = math.floor(tester.n*1.41)
    test_cases = tester.get_test_cases()
    store_test_cases(filepath="test_cases/increasing_n_and_m_200.json", test_cases=test_cases)"""

    # code to load the test cases
    test_cases = load_test_cases("test_cases/increasing_n_and_m_200.json")

    plot_data_list = Analyzer.analyze_schedulers(Schedulers_To_Test, test_cases, normalized=True)
    x_values = [test_case.x_value for test_case in test_cases]
    Plotter.plot_graph(plot_data_list, x_values, x_label="n", y_label="normalized Makespan", x_scale="log")
    Plotter.plot_table(data_list=[plot_data.means for plot_data in plot_data_list], 
                       column_labels=["List_Scheduler","LTF_Scheduler","Shelf_Scheduler", "JR_Scheduler", "Tower_Scheduler"], row_labels=x_values)
    
    # -------- Generate Figure ---------- #
    figure, axis = Plotter.begin_plotting(Schedulers_To_Test,x_label="n", y_label="normalized Makespan", x_scale="log")
    for m, color in [(5,'b'), (10,'g'),(25,'y'),(50,'r'),(500,'k')]:
        # code to generate and store the test cases
        """tester = Tester(m=m,n=10,p_min=0,p_max=1,q_min=1,q_max=m)
        for _ in range(number_of_test_cases):
            tester.generate_one_test_case(number_of_instances_per_test_case, float_execution_time=True, x_value=tester.n)
            tester.n = math.floor(tester.n*1.41)
        test_cases = tester.get_test_cases()
        store_test_cases(filepath="test_cases/increasing_n_and_m_" + str(m)+".json", test_cases=test_cases)"""
        
        # code to load the test cases
        test_cases = load_test_cases("test_cases/increasing_n_and_m_" + str(m)+".json")

        plot_data_list = Analyzer.analyze_schedulers(Schedulers_To_Test, test_cases, normalized=True)
        x_values = [test_case.x_value for test_case in test_cases]

        Plotter.plot_graphs(figure,axis, plot_data_list,x_values,color=color)

    figure.subplots_adjust(wspace=20)
    plt.show()

    # -------- Generate Figure ---------- #
    figure, axis = Plotter.begin_plotting(Schedulers_To_Test,x_label="m", y_label="normalized Makespan", x_scale="log")
    for n, color in [(5,'b'), (10,'g'),(25,'y'),(50,'r'),(500,'k')]:
        # code to generate and store the test cases
        """tester = Tester(m=10,n=n,p_min=0,p_max=1,q_min=1,q_max=10)
        for _ in range(number_of_test_cases):
            tester.generate_one_test_case(number_of_instances_per_test_case, float_execution_time=True, x_value=tester.m)
            tester.m = math.floor(tester.m*1.41)
            tester.q_max=tester.m
        test_cases = tester.get_test_cases()
        store_test_cases(filepath="test_cases/increasing_m_and_n_" + str(n)+".json", test_cases=test_cases)"""
        
        # code to load the test cases
        test_cases = load_test_cases("test_cases/increasing_m_and_n_" + str(n)+".json")

        plot_data_list = Analyzer.analyze_schedulers(Schedulers_To_Test, test_cases, normalized=True)
        x_values = [test_case.x_value for test_case in test_cases]

        Plotter.plot_graphs(figure,axis, plot_data_list,x_values,color=color)

    figure.subplots_adjust(wspace=20)
    plt.show()
    
    # -------- Generate Figure ---------- #
    # code to generate and store the test cases
    """tester = Tester(m=200,n=500,p_min=0,p_max=1,q_min=1,q_max=200)
    for _ in range(number_of_test_cases):
        tester.generate_one_test_case(number_of_instances_per_test_case, float_execution_time=True, x_value=tester.q_min)
        tester.q_min += 6
    test_cases = tester.get_test_cases()
    store_test_cases(filepath="test_cases/increasing_q_min.json", test_cases=test_cases)"""

    # code to load the test cases
    test_cases = load_test_cases("test_cases/increasing_q_min.json")

    plot_data_list = Analyzer.analyze_schedulers(Schedulers_To_Test, test_cases, normalized=True)
    x_values = [test_case.x_value for test_case in test_cases]
    Plotter.plot_graph(plot_data_list, x_values, x_label="q_min", y_label="normalized Makespan", x_scale="linear")

    # -------- Generate Figure ---------- #
    # code to generate and store the test cases
    """tester = Tester(m=200,n=500,p_min=0,p_max=1,q_min=1,q_max=200)
    for _ in range(number_of_test_cases):
        tester.generate_one_test_case(number_of_instances_per_test_case, float_execution_time=True, x_value=tester.q_max)
        tester.q_max -= 12
    test_cases = tester.get_test_cases()
    store_test_cases(filepath="test_cases/increasing_q_max.json", test_cases=test_cases)"""
    
    # code to load the test cases
    test_cases = load_test_cases("test_cases/increasing_q_max.json")

    plot_data_list = Analyzer.analyze_schedulers(Schedulers_To_Test, test_cases, normalized=True)
    x_values = [test_case.x_value for test_case in test_cases]
    Plotter.plot_graph(plot_data_list, x_values, x_label="q_max", y_label="normalized Makespan", x_scale="linear")



    # jobs = load_jobs('data.json')

    #jobs = Scheduler.generate_random_jobs(number_of_jobs=200,min_execution_time=1,max_execution_time=10,
    #                                                min_required_machines=1,max_required_machines=20)
    #visualize_scheduler(LIST_Scheduler, num_machines=40, jobs=jobs)


 