from copy import deepcopy


class Alignment:

    def __init__(self):
        self.log_path = []
        self.model_path = []
        self.cost = 0
        self.processed_events = 0

    def sync_move(self, activity):
        self.log_path.append(activity)
        self.model_path.append(activity)
        self.processed_events = self.processed_events + 1
        return self

    def log_move(self, activity):
        self.log_path.append(">")
        self.model_path.append(activity)
        self.cost = self.cost + 1
        self.processed_events = self.processed_events + 1
        return self

    def model_move(self, activity):
        self.log_path.append(activity)
        self.model_path.append(">")
        self.cost = self.cost + 1
        self.processed_events = self.processed_events + 1
        return self

    def __add__(self, other):
        alignment = Alignment()
        alignment.log_path = deepcopy(self.log_path)
        alignment.log_path.extend(other.log_path)
        alignment.model_path = deepcopy(self.model_path)
        alignment.model_path.extend(other.model_path)
        alignment.cost = deepcopy(self.cost)
        alignment.cost = alignment.cost + other.cost
        alignment.processed_events = deepcopy(self.processed_events)
        alignment.processed_events = alignment.processed_events + other.processed_events
        return alignment

    def __len__(self):
        return self.processed_events

    def __lt__(self, other):
        return self.cost < other.cost

    def __str__(self):
        return f"log: {self.log_path}\nmdl: {self.model_path}"