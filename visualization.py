from PIL import Image, ImageDraw 
from typedefs import *
import secrets

unit_size = 10

# from the bottom left of the image
coord_system_start_x = 100 
coord_system_start_y = 100

# to make the rectangles smaller so that the outlines can be seen
epsilon = 1

# requires that jobs have integer exeuction times
# example usage: visualize_scheduler(LIST_Scheduler, num_machines=40, jobs=jobs)
def visualize_scheduler(Scheduler_To_Visualize, num_machines, jobs):
    # calculate makespan
    scheduler = Scheduler_To_Visualize(num_machines, jobs, CREATE_SCHEDULE=True)
    makespan = scheduler.schedule()
    print("makespan:", makespan)

    # create image
    scheduling_image = Scheduling_Image(num_machines*unit_size + 2*coord_system_start_x, makespan*unit_size + 2*coord_system_start_y)
    scheduling_image.draw_axes()
    scheduling_image.draw_border(num_machines)
    scheduling_image.draw_schedule(scheduler.get_schedule())
    scheduling_image.create_image()


class Scheduling_Image:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.image = Image.new("RGB", (width,height))
        self.image_draw = ImageDraw.Draw(self.image)
    
    def draw_axes(self):
        x_axis = [(100, 100), (100, self.height-100)]
        y_axis = [(100, self.height-100), (self.width-100, self.height-100)]
        self.image_draw.line(x_axis, fill ="#ffffff", width=1)
        self.image_draw.line(y_axis, fill ="#ffffff", width=1)

        # draw marker at every integer position on the axis
        marker_size = 5

        # draw marker y
        marker_number = 0
        for i in range((self.height-200-1)//unit_size,0,-1):
            marker_number +=1
            updated_marker_size = marker_size
            marker_color = "#ffffff"
            if marker_number%100 == 0:
                updated_marker_size +=2
                marker_color = "#ff0000"
            elif marker_number %10 == 0:
                updated_marker_size +=1
                marker_color = "#00ff00"

            line = [(100-updated_marker_size, 100+i*unit_size),(100+updated_marker_size,100+i*unit_size)]
            self.image_draw.line(line,fill=marker_color,width=1)

        # draw marker x
        for i in range(1, (self.width-200)//unit_size):
            line = [(100+i*unit_size, self.height-100-marker_size),(100+i*unit_size, self.height-100+marker_size)]
            self.image_draw.line(line,fill="#ffffff",width=1)

    # adds a vertical line to see how many machine there are
    def draw_border(self,m):
        border = [(100+m*unit_size, 100), (100+m*unit_size, self.height-100)]
        self.image_draw.line(border, fill ="#aa0000", width=1)

    def draw_schedule(self, schedule : Schedule):
        placed_jobs  = schedule.placed_jobs

        for placed_job in placed_jobs:
            indices = placed_job.machine_indices
            job     = placed_job.job
            height  = placed_job.starting_time

            random_color = "#" + secrets.token_hex(3)
            for index in indices:
                rectangle = self.__create_rectangle(index, height, 1, job.execution_time)
                self.image_draw.rectangle(rectangle, fill=random_color, outline="black")


    def create_image(self):
        self.image.show()

    # converts 2d list indices the points on the image (starting at the origin of the coordinate system) 
    # i is the x-coordinate, j the y-coordinate, w the width (added to the right) and h the height (added to the top)
    def __create_rectangle(self,i,j,w,h):
        return [(coord_system_start_x + i*unit_size+epsilon, self.height - coord_system_start_y -j*unit_size - h*unit_size+epsilon),
            (coord_system_start_x + (i+w)*unit_size-epsilon, self.height - coord_system_start_y -j*unit_size-epsilon)]
