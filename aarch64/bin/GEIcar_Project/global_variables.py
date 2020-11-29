from threading import Lock, Event

class mutex_variable:
    def __init__(self):
        self.value = 0
        self.MUT = Lock()



detection_flag = mutex_variable()
detection_flag.value = 1

pub = mutex_variable()
input = mutex_variable()

tab_delta_time_loop_human = []
tab_delta_time_loop_hurdles = []
tab_delta_time_loop_ROS = []

NUMBER_OF_LOOPS_FOR_TEST = 100

loop_counter_human = 0
loop_counter_hurdles = 0
loop_counter_ROS = 0
