from copy import deepcopy

from algorithm.align_path_store import AlignmentStates
from algorithm.petri_net import DistributedPetriNet
from algorithm.protocol.conformance_protocol import ConformanceProtocol
from algorithm.service.alignment_path_service import AlignmentPathService
from distributed_environment_builder.infrastructure.network import Network

class ConformanceService:

    def __init__(self, network: Network[ConformanceProtocol], alignment_delay: int, node_id: str):
        self.alignment_states = AlignmentStates()
        self.alignment_delay: int = alignment_delay
        self.total_events_received = 0
        self.alignment_path_service = AlignmentPathService(network, node_id)
        self.network = network

    def calculate_conformance(self, case: str, activity: str, petri_net: DistributedPetriNet):
        self.total_events_received = self.total_events_received + 1
        alignment_states = self.alignment_states
        if alignment_states.is_empty(case):
            alignment_states.init_case(case, petri_net.initial_places)
        if self.alignment_states.size() <= self.alignment_delay:
            return alignment_states
        self.alignment_states = self.iterate_alignment_states(alignment_states, case, activity, petri_net)
        return self.alignment_states

    def iterate_alignment_states(self, alignment_states, case, activity, petri_net):
        next_align_paths = []
        while not alignment_states.is_empty(case):
            align_path = alignment_states.pop_align_state(case)
            next_align_paths.extend(self.find_alignment(case, activity, petri_net, align_path, True))
        for path in next_align_paths:
            alignment_states.push_align_path(case, path)
        return deepcopy(alignment_states)

    def find_alignment(self, case, activity, petri_net, align_path, eval_external):
        paths = []
        sync_move_path = self.alignment_path_service.sync_move(activity, petri_net, align_path, case, eval_external)

        if petri_net.is_activity_in_net(activity) and activity not in self.network.get_all_node_ids():
            log_move_path = self.alignment_path_service.log_move(activity, align_path)
        else:
            log_move_path = None

        model_move_path = self.alignment_path_service.model_move(case, activity, petri_net, align_path, eval_external)
        paths.extend([path for path in [sync_move_path, log_move_path, model_move_path] if path is not None])
        return paths

    def get_conformance_for_case(self, case) -> int:
        return self.alignment_states.get_minimal_cost(case)

    def get_conformance_to_end_for_case(self, case, petri_net, target_node) -> int:
        if self.alignment_states.size_of_case(case) == 0:
            return 0
        paths = self.find_alignment(
                case,
                target_node,
                petri_net,
                self.alignment_states.top(case),
                eval_external=False
            )
        if not paths:
            return 0
        return min([path.cost() for path in paths])

    def get_alignment_states(self) -> AlignmentStates:
        return self.alignment_states
