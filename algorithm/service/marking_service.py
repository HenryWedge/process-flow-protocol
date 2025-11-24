from typing import List
from algorithm.align_path_store import AlignmentStates
from algorithm.network_predecessor import NetworkPredecessor
from algorithm.protocol.conformance_protocol import ConformanceProtocol
from algorithm.petri_net import DistributedPetriNet
from distributed_environment_builder.infrastructure.network import Network
from process_mining_core.datastructure.core.event import Event

class MarkingService:

    def __init__(self, network: Network[ConformanceProtocol]):
        self.network: Network[ConformanceProtocol] = network
        self.last_timestamp = {}

    def update_marking(
        self,
        event: Event,
        petri_net: DistributedPetriNet,
        alignment_path_store: AlignmentStates
    ):
        newly_marked_places = []
        newly_marked_places.extend(self.check_initial_markings(event.activity, petri_net))
        newly_marked_places.extend(self.check_inbound_markings(event.caseid, petri_net))

        #TODO hrei: That needs some optimization. I dont like this solution at the moment
        for place in newly_marked_places:
            alignment_path_store.mark_place(event.caseid, place=place[0])

        self.last_timestamp[event.caseid] = event.timestamp

    def check_initial_markings(
        self,
        activity: str,
        petri_net: DistributedPetriNet
    ):
        newly_marked_places = []
        for place in petri_net.get_places_before_activity(activity):
            if place in petri_net.initial_places:
                newly_marked_places.append((place, 0))
        return newly_marked_places

    def check_inbound_markings(self, case_id: str, petri_net: DistributedPetriNet):
        newly_marked_places = []
        predecessor = self.find_predecessor_node(case_id, petri_net)
        if not predecessor or (case_id in self.last_timestamp and predecessor.last_timestamp < self.last_timestamp[case_id]):
            return []
        cost = predecessor.send(self.network).get_conformance_to_end_for_case(case_id)
        places = petri_net.get_places_after_activity(predecessor.node_id)
        for place in places:
            newly_marked_places.append((place, cost))
        return newly_marked_places

    def find_predecessor_node(self, case_id: str, petri_net: DistributedPetriNet):
        predecessors = [NetworkPredecessor(node_id=transition.activity_label)
                        for transition in petri_net.get_transitions_missing_inbound_place()]
        network_predecessors: List[NetworkPredecessor[ConformanceProtocol]] = []

        for network_predecessor in predecessors:
            last_timestamp = network_predecessor.send(self.network).get_time_for_case(case_id)
            if last_timestamp:
                network_predecessor.update_last_timestamp(last_timestamp)
                network_predecessors.append(network_predecessor)

        if network_predecessors:
            return max(network_predecessors)
        return None