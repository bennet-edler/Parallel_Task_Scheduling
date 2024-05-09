from approximate_scheduler.base_scheduler import Scheduler
from approximate_scheduler.ltf_nc import Longest_Task_First_Scheduler_NC
from approximate_scheduler.ltf_c import Longest_Task_First_Scheduler_C
from approximate_scheduler.list import LIST_Scheduler
from optimal_scheduler.not_fragmentable import Not_Fragmentable_Scheduler
from optimal_scheduler.fragmentable import Fragmentable_Scheduler
from scheduling_image import Scheduling_Image
from typedefs import Schedule

if __name__ == "__main__":

    # generate random jobs
    jobs = Scheduler.generate_random_jobs(
            number_of_jobs=5, min_execution_time=1, max_execution_time=40,
            min_required_machines=1, max_required_machines=3)
    m = 5

    # calculate makespan
    scheduler = Not_Fragmentable_Scheduler(m, jobs, CREATE_SCHEDULE=True)
    print("makespan:", scheduler.schedule())

    # create image
    scheduling_image = Scheduling_Image(1920//2, 6*1080)
    scheduling_image.draw_axes()
    scheduling_image.draw_border(m)
    scheduling_image.draw_schedule(scheduler.get_schedule())
    scheduling_image.create_image()


 