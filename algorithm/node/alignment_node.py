from collections import deque
from copy import deepcopy
from typing import List, Dict

from algorithm.hidden_event import HiddenEvent
from algorithm.node.alignment import Alignment
from algorithm.petri_net import DistributedPetriNet
from algorithm.petri_net_converter import PetriNetConverter
from algorithm.petri_net_utils import Marking, Transition
from algorithm.strategy.discovery.discovery_strategy import DiscoveryStrategy
from algorithm.strategy.discovery.heuritics_miner_discovery_strategy import HeuristicsMinerDiscoveryStrategy
from distributed_environment_builder.infrastructure.network import Network
from network_node import NetworkNode
from process_mining_core.datastructure.core.event import Event

class AlignmentNode(NetworkNode):

    def __init__(self, node_id, network):
        super().__init__(node_id, network)
        self.node_id = node_id
        self.network: Network = network
        self.global_event_log: Dict[str, List[Event]] = {}
        self.local_event_log: Dict[str, List[Event]] = {}
        self.petri_net: DistributedPetriNet = None
        self.alignment_model: Dict[str, DistributedPetriNet] = {}
        self.marking: Dict[str, Marking] = {}
        self.discovery_strategy: DiscoveryStrategy = HeuristicsMinerDiscoveryStrategy()

    def receive_event(self, event: Event):
        case_id = event.caseid
        if not case_id in self.global_event_log:
            self.global_event_log[case_id] = []
        if not case_id in self.local_event_log:
            self.local_event_log[case_id] = []
        self.local_event_log[case_id].append(HiddenEvent(event))
        self.learn_model(event)

    def _convert_event_log(self):
        result = []
        for key in self.global_event_log:
            for event in self.global_event_log[key]:
                result.append(event)
        return result

    def learn_model(self, event):
        case_id = event.caseid
        longest_event_log = []
        for node in self.network.get_all_nodes(self.node_id):
            event_log = node.get_event_log_for_case(case_id)
            if len(event_log) > len(longest_event_log):
                longest_event_log = event_log
        longest_event_log.append(HiddenEvent(event))
        self.global_event_log[case_id] = longest_event_log
        self.model, self.im, self.fm = self.discovery_strategy.discover(self._convert_event_log())

    def get_event_log_for_case(self, case: str) -> List[Event]:
        if not case in self.global_event_log:
            return []
        return deepcopy(self.global_event_log[case])

    def align_event(self, event):
        event = HiddenEvent(event)
        case_id = event.caseid
        self.get_alignment_model(case_id)

        alignment = Alignment()
        return self.get_alignment_of_event(case_id, event.activity, alignment)

    def get_alignment_model(self, case_id):
        if not case_id in self.alignment_model:
            self.alignment_model[case_id] = self.model, self.im, self.fm
        return self.alignment_model[case_id]

    def get_local_log(self, case_id):
        if not case_id in self.local_event_log:
            self.local_event_log[case_id] = []
        return self.local_event_log[case_id]

    def get_alignment_of_event(self, case_id: str, target: str, alignment: Alignment):
        model, im, fm = self.get_alignment_model(case_id)
        log = self.get_local_log(case_id)

        petri_net = PetriNetConverter().convert(model, im, fm, [])

        start_transitions = petri_net.get_transitions_after_place(petri_net.initial_places)
        start_transition = [t for t in start_transitions if t.activity_label][0]
        path = self.bfs_shortest_path_between_activities_reverse(petri_net, target, start_transition.activity_label)

        for transition in path:
            external_node = None
            if self.node_id in transition.activity_label:
                alignment = alignment + self.calculate_alignment([transition], log)
            else:
                for node_id in self.network.get_all_node_ids():
                    if node_id in transition.activity_label:
                        external_node = node_id
                if external_node:
                    alignment = alignment + self.network.get_node(external_node).get_alignment_of_event(
                        case_id=case_id, target=deepcopy(transition.activity_label), alignment=Alignment()
                    )
        return alignment

    def calculate_alignment(self, model_path: List[Transition], log_path: List[Event]) -> Alignment:
        if not model_path:
            alignment = Alignment()
            for event in log_path:
                alignment.log_move(event.activity)
            return alignment
        if not log_path:
            alignment = Alignment()
            for transition in model_path:
                alignment.model_move(transition.activity_label)
            return alignment

        if model_path[-1].activity_label == log_path[-1].activity:
            return self.calculate_alignment(deepcopy(model_path[0:-1]), deepcopy(log_path[0:-1])).sync_move(
                log_path[-1].activity)

        return min(
            self.calculate_alignment(deepcopy(model_path[0:-1]), deepcopy(log_path)).model_move(
                deepcopy(model_path[-1].activity_label)),
            self.calculate_alignment(deepcopy(model_path), deepcopy(log_path[0:-1])).log_move(
                deepcopy(log_path[-1].activity)),
        )

    def bfs_shortest_path_between_activities_reverse(self, petri_net, final_activity, start_activity):
        place_marking = {}
        final_transition = petri_net.get_transition_for_activity(final_activity)[0]
        for input_place in final_transition.output_places:
            place_marking[input_place] = 1
        final_marking = Marking(place_marking)
        target_transition = petri_net.get_transition_for_activity(start_activity)[0]
        if petri_net.is_enabled_reverse(final_marking, target_transition):
            return [target_transition]

        queue = deque([(final_marking, [])])
        visited_markings = {final_marking}

        while queue:
            current_marking, current_path = queue.popleft()
            enabled_transitions = petri_net.get_enabled_transitions_reverse(current_marking)
            for t in enabled_transitions:
                next_marking = petri_net.fire_reverse(current_marking, t)
                if next_marking not in visited_markings:
                    visited_markings.add(next_marking)
                    new_path = current_path + [t]
                    if petri_net.is_enabled_reverse(next_marking, target_transition):
                        new_path.append(target_transition)
                        return new_path
                    queue.append((next_marking, new_path))
        return None
