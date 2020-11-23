from threading import Lock, Event

class detection_number_class:
    def __init__(self):
        self.value = 0
        self.MUT = Lock()

detection_number = detection_number_class()

detection_done = Event()
sending_done = Event()

pub = 0

tab_delta_time_loop = []
