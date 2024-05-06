from scheduler.base_scheduler import Scheduler
from scheduler.ltf_nc import Longest_Task_First_Scheduler_NC
from scheduler.ltf_c import Longest_Task_First_Scheduler_C
from scheduler.list import LIST_Scheduler
from scheduling_image import Scheduling_Image
from typedefs import Schedule

if __name__ == "__main__":

    # generate random jobs
    jobs = Scheduler.generate_random_jobs(
            number_of_jobs=100, min_execution_time=1, max_execution_time=40,
            min_required_machines=1, max_required_machines=10)
    m = 30

    # calculate makespan
    scheduler = LIST_Scheduler(m, jobs, create_schedule=True)
    print("makespan:", scheduler.schedule())

    # create image
    scheduling_image = Scheduling_Image(1920//2, 6*1080)
    scheduling_image.draw_axes()
    scheduling_image.draw_border(m)
    scheduling_image.draw_schedule(scheduler.get_schedule())
    scheduling_image.create_image()


 