from threading import Lock, Event

class mutex_variable:
    def __init__(self):
        self.value = 0
        self.MUT = Lock()



detection_flag = mutex_variable()
detection_flag.value = 1

pub = mutex_variable()

tab_delta_time_loop = []
