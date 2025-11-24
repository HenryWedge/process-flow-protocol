from collections import deque
from copy import deepcopy

from algorithm.petri_net import DistributedPetriNet
from algorithm.petri_net_utils import AlignPath
from algorithm.protocol.conformance_protocol import ConformanceProtocol
from distributed_environment_builder.infrastructure.network import Network


class AlignmentPathService:

    def __init__(self, network: Network[ConformanceProtocol], node_id: str):
        self.network = network
        self.node_id = node_id

    def log_move(self, activity, align_path):
        this_align_path = deepcopy(align_path)
        this_align_path.log_move(activity)
        return this_align_path

    def sync_move(self, activity: str, petri_net: DistributedPetriNet, align_path: AlignPath, case, eval_external):
        this_align_path = deepcopy(align_path)

        transition_to_activity = petri_net.get_transition_for_activity(activity)
        if not transition_to_activity:
            return None

        if petri_net.can_fire_activity(activity, this_align_path.marking):
            marking = petri_net.fire(this_align_path.marking, transition_to_activity[0])
        else:
            transitions = []
            for t in transition_to_activity:
                trans = (
                    self._bfs_shortest_silent_path_to_transition(
                        petri_net=petri_net,
                        initial_marking=this_align_path.marking,
                        target_transition=t
                    ))
                if trans:
                    transitions.extend(trans)
                    transitions.extend(transition_to_activity)
            if not transitions:
                return None
            else:
                marking = this_align_path.marking
                for transition in transitions:
                    marking = petri_net.fire(marking, transition)

        if eval_external and activity in self.network.get_all_node_ids():
            external_cost = self.network.get_node(activity).get_conformance_to_end_for_case(case, self.node_id)
            this_align_path.external_move(activity, external_cost)
        else:
            this_align_path.sync_move(activity)

        this_align_path.update_marking(marking)

        return this_align_path

    def model_move(
            self,
            case: str,
            activity: str,
            petri_net: DistributedPetriNet,
            align_path: AlignPath,
            eval_external: bool
    ):
        this_align_path = deepcopy(align_path)
        if not petri_net.is_activity_in_net(activity):
            return None
        target_transitions = petri_net.get_transition_for_activity(activity)
        target_transition = target_transitions[0]
        marking = this_align_path.marking
        path = self._bfs_shortest_path_to_transition(petri_net, marking, target_transition)
        if not path:
            return None
        if eval_external:
            path.append(target_transition)
        new_marking = petri_net.fire_multiple(marking, path)

        for transition in path:
            this_align_path.model_move(transition.activity_label)

        if eval_external and target_transition.activity_label in self.network.get_all_node_ids():
            external_cost = self.network.get_node(target_transition.activity_label).get_conformance_to_end_for_case(case, self.node_id)
            this_align_path.external_move(target_transition.activity_label, external_cost)
        else:
            this_align_path.sync_move(target_transition.activity_label)

        this_align_path.update_marking(new_marking)
        return this_align_path


    def _bfs_shortest_path_to_transition(self, petri_net, initial_marking, target_transition):
        if petri_net.is_enabled(initial_marking, target_transition):
            return []

        queue = deque([(initial_marking, [])])
        visited_markings = {initial_marking}

        while queue:
            current_marking, current_path = queue.popleft()
            enabled_transitions = petri_net.get_enabled_transitions(current_marking)
            for t in enabled_transitions:
                next_marking = petri_net.fire(current_marking, t)
                if next_marking not in visited_markings:
                    visited_markings.add(next_marking)
                    new_path = current_path + [t]
                    if petri_net.is_enabled(next_marking, target_transition):
                        return new_path
                    queue.append((next_marking, new_path))
        return None


    def _bfs_shortest_silent_path_to_transition(self, petri_net, initial_marking, target_transition):
        if petri_net.is_enabled(initial_marking, target_transition):
            return []

        queue = deque([(initial_marking, [])])
        visited_markings = {initial_marking}

        while queue:
            current_marking, current_path = queue.popleft()
            enabled_transitions = petri_net.get_activatable_silent_transitions(current_marking)
            for t in enabled_transitions:
                next_marking = petri_net.fire(current_marking, t)
                if next_marking not in visited_markings:
                    visited_markings.add(next_marking)
                    new_path = current_path + [t]
                    if petri_net.is_enabled(next_marking, target_transition):
                        return new_path
                    queue.append((next_marking, new_path))
        return None
