import json
from typing import Dict, List, Set


class Marking:
    def __init__(self, place_marking):
        self.place_marking: Dict[str, int] = place_marking

    def __eq__(self, other):
        return self.place_marking == other.place_marking

    def __hash__(self):
        return hash(json.dumps(self.place_marking, sort_keys=True))

    def active_places(self):
        active_places = set()
        for place_marking in self.place_marking:
            if self.place_marking[place_marking] > 0:
                active_places.add(place_marking)
        return active_places

    def mark_place(self, place):
        if place in self.place_marking:
            self.place_marking[place] = self.place_marking[place] + 1
        else:
            self.place_marking[place] = 1

    def mark_places(self, places):
        for place in places:
            self.mark_place(place)

    def get_markings_of_place(self, place):
        if not place in self.place_marking:
            return 0
        return self.place_marking[place]

    def is_marked(self, place):
        return self.get_markings_of_place(place) > 0

    def move(self, from_places, to_places):
        for from_place in from_places:
            if from_place not in self.place_marking:
                self.place_marking[from_place] = 0
            self.place_marking[from_place] = self.place_marking[from_place] - 1
        for to_place in to_places:
            if to_place not in self.place_marking:
                self.place_marking[to_place] = 0
            self.place_marking[to_place] = self.place_marking[to_place] + 1
        if self.place_marking[from_place] < 0:
            print("Warning marking illegal")
        return self

    def __str__(self):
        return f"Marking: {self.place_marking}"

class Transition:
    def __init__(self, activity_label, input_places, output_places):
        self.activity_label: str = activity_label
        self.input_places: Set[str] = input_places
        self.output_places: Set[str] = output_places

    def is_activatable(self, marking: Marking, activity: str):
        for input_place in self.input_places:
            if not input_place in marking.active_places():
                return False
        return activity == self.activity_label

    def is_activatable_without_activity(self, marking: Marking):
        for input_place in self.input_places:
            if not input_place in marking.active_places():
                return False
        return True

class ReceivingPlace:
    def __init__(self, name, predecessor):
        self.name = name
        self.predecessor = predecessor

class AlignState:
    def __init__(self, marking: Marking):
        self.marking: Marking = marking
        self.log_path = []
        self.model_path = []
        self.cost = 0

    def __lt__(self, other):
        return self.cost < other.cost

class AlignPath:
    def __init__(self, initial_marking):
        self.log_path = []
        self.model_path = []
        self.marking = initial_marking
        self.input_cost = 0
        self.external_cost = 0

    def mark_place(self, place):
        self.marking.mark_place(place)

    def sync_move(self, activity):
        self.model_path.append(activity)
        self.log_path.append(activity)

    def external_move(self, activity, external_cost):
        self.model_path.append(activity)
        self.log_path.append(activity)
        self.external_cost = self.external_cost + external_cost

    def model_move(self, model_move: str):
        self.model_path.append(model_move)
        self.log_path.append(">")

    def log_move(self, log_move: str):
        self.model_path.append(">")
        self.log_path.append(log_move)

    def cost(self):
        cost = 0
        for activity in self.log_path:
            if activity == ">":
                cost = cost + 1
        for activity in self.model_path:
            if activity == ">":
                cost = cost + 1
        return self.external_cost + cost

    def add_input_cost(self, cost):
        self.input_cost = self.input_cost + cost

    def update_marking(self, marking: Marking):
        self.marking = marking

    def __str__(self):
        return f"Alignment: \nLog move: {self.log_path}\nMdl move: {self.model_path}\nCost: {self.cost()}\nInput cost: {self.external_cost}\nMarking: {self.marking}"

    def __lt__(self, other):
        return self.cost() < other.cost()