from collections import deque
from copy import deepcopy
from typing import List, Set

from algorithm.petri_net_utils import Marking, Transition, AlignPath

class DistributedPetriNet:

    def __init__(
        self,
        transitions: List[Transition],
        initial_places: Set[str],
        inbound_places: List[str],
        outbound_places: List[str]
    ):
        self.transitions = transitions
        self.initial_places: Set[str] = initial_places
        self.inbound_places: List[str] = inbound_places
        self.outbound_places: List[str] = outbound_places

    def get_places_before_activity(self, activity):
        input_place_list = [transition.input_places for transition in self.transitions if transition.activity_label == activity]
        return [input_place for input_places in input_place_list for input_place in input_places]

    def get_places_after_activity(self, activity):
        output_place_list = [transition.output_places for transition in self.transitions if transition.activity_label == activity]
        return [output_place for outbound_places in output_place_list for output_place in outbound_places]

    def get_activity_before_place(self, place):
        return [transition.activity_label for transition in self.transitions if place in transition.output_places]

    def get_transition_for_activity(self, activity):
        return [transition for transition in self.transitions if transition.activity_label == activity]

    def get_silent_transitions(self):
        return [transition for transition in self.transitions if transition.activity_label == None]

    def is_activity_in_net(self, activity):
        return len(self.get_transition_for_activity(activity)) > 0

    def can_fire_activity(self, activity, marking: Marking) -> bool:
        for transition in self.get_transition_for_activity(activity):
            if self.is_enabled(marking, transition):
                return True
        return False

    def get_activatable_silent_transitions(self, marking: Marking) -> List[Transition]:
        silent_transitions = []
        for transition in self.get_silent_transitions():
            if self.is_enabled(marking, transition):
                silent_transitions.append(transition)
        return silent_transitions


    def is_enabled(self, marking, transition):
        for input_place in transition.input_places:
            if not marking.is_marked(input_place):
                return False
        return True

    def get_enabled_transitions(self, marking):
        enabled = []
        for transition in self.transitions:
            if self.is_enabled(marking, transition):
                enabled.append(transition)
        return enabled

    def get_enabled_input_transitions(self, marking):
        return [transition for transition in self.get_enabled_transitions(marking) if "input_" in transition.activity_label]

    def get_transitions_missing_inbound_place(self):
        activatable_transitions = []
        for transition in self.transitions:
            if transition.activity_label in self.inbound_places:
                activatable_transitions.append(transition)
        return activatable_transitions

    def fire(self, marking, transition):
        this_marking = deepcopy(marking)
        this_marking.move(transition.input_places, transition.output_places)
        return this_marking

    def fire_multiple(self, marking, transitions):
        this_marking = deepcopy(marking)
        for transition in transitions:
            this_marking = self.fire(this_marking, transition)
        return this_marking

    def bfs_shortest_path_to_transition(self, initial_marking, target_transition):
        if self.is_enabled(initial_marking, target_transition):
            return []

        queue = deque([(initial_marking, [])])
        visited_markings = {initial_marking}

        while queue:
            current_marking, current_path = queue.popleft()
            enabled_transitions = self.get_enabled_transitions(current_marking)
            for t in enabled_transitions:
                next_marking = self.fire(current_marking, t)
                if next_marking not in visited_markings:
                    visited_markings.add(next_marking)
                    new_path = current_path + [t]
                    if self.is_enabled(next_marking, target_transition):
                        return new_path
                    queue.append((next_marking, new_path))
        return None
