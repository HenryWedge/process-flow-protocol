from typing import List, Dict, Any

import pm4py.discovery
from pm4py import PetriNet, Marking

from algorithm.predecessor_utility import PredecessorUtility
from algorithm.protocol.conformance_protocol import ConformanceProtocol
from distributed_environment_builder.infrastructure.network import Network
from network_node import NetworkNode
from process_mining_core.converter.pm4py_converter import Pm4PyConverter
from process_mining_core.datastructure.core.event import Event

class GroundTruthNode(NetworkNode, ConformanceProtocol):
    def __init__(self, node_id: str, network: Network[ConformanceProtocol]):
        super().__init__(node_id, network)
        self.event_log: List[Event] = []
        self.models: Dict[str, Any] = {}
        self.current_cases = {}
        self.conformance_values: Dict[str, int] = {}
        self.timestamp_for_case: Dict[str, Any] = {}

    def receive_event(self, event: Event):
        predecessor_cost = 0
        case_id = event.caseid
        if not case_id in self.current_cases:
            self.current_cases[case_id] = []
        predecessor = self.get_predecessor(case_id)

        if predecessor:
            incoming_event = Event(
                case_id=event.caseid,
                activity=predecessor.node_id,
                timestamp=predecessor.last_timestamp,
                node="",
                group_id=""
            )
            self.event_log.append(incoming_event)
            #self.current_cases[case_id].append(incoming_event)
            self.confirm_predecessor(case_id, self.node_id, event.timestamp)

        self.timestamp_for_case[case_id] = event.timestamp
        self.event_log.append(event)
        self.current_cases[case_id].append(event)
        if not case_id in self.models:
            self.models[case_id] = pm4py.discovery.discover_petri_net_inductive(Pm4PyConverter().from_event_log(self.event_log))

        if case_id in self.models:
            net, im, fm = self.models[case_id]
        else:
            net, im, fm = pm4py.discover_petri_net_inductive(Pm4PyConverter().from_event_log([]))

        alignment = pm4py.conformance.conformance_diagnostics_alignments(
            Pm4PyConverter().from_event_log(self.current_cases[case_id]), net, im, fm)[0]
        alignment_cost = alignment['cost']

        if predecessor:
            predecessor_cost = predecessor.send(self.network).get_conformance_for_case(case_id)

        self.conformance_values[case_id] = alignment_cost + predecessor_cost
        print(f"Node: {self.node_id}")
        print(f"Cost: {self.conformance_values[case_id]}")


    def learn(self):
        pass

    def get_conformance(self):
        pass

    def get_predecessor(self, case_id):
        predecessor = PredecessorUtility().find_predecessor(
            network=self.network, case=case_id, own_id=self.node_id
        )
        if (predecessor and
                (not self.current_cases[case_id] or
                 (len(self.current_cases[case_id]) >= 1
                  and self.current_cases[case_id][-1].timestamp < predecessor.last_timestamp))
        ):
            return predecessor
        return None

    def get_time_for_case(self, case) -> str:
        if not case in self.current_cases:
            return None
        return self.current_cases[case][-1].timestamp

    def get_conformance_for_case(self, case) -> int:
        if not case in self.conformance_values:
            return 0
        return self.conformance_values[case]

    def get_conformance_to_end_for_case(self, case, node_name) -> int:
        pass
        # pm4py.conformance.conformance_diagnostics_alignments(
        #    Pm4PyConverter().from_event_log(self.current_cases[case]), net, im, fm
        # )[0]

    def confirm_predecessor(self, case, node_name, time):
        pass
        #self.event_log.append(
        #    Event(
        #        case_id=case,
        #        activity=node_name,
        #        timestamp=time,
        #        node="",
        #        group_id=""
        #    )
        #)
