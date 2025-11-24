from typing import List, Dict, Any

import pm4py.discovery

from distributed_environment_builder.infrastructure.network import Network
from network_node import NetworkNode
from process_mining_core.converter.pm4py_converter import Pm4PyConverter
from process_mining_core.datastructure.core.event import Event

class DistributedNode(NetworkNode):

    def __init__(self, node_id: str, network: Network):
        super().__init__(node_id, network)
        self.event_log: List[Event] = []
        self.models: Dict[str, Any] = {}
        self.current_cases = {}

    def receive_event(self, event: Event):
        case_id = event.caseid
        self.event_log.append(event)

        if not case_id in self.current_cases:
            self.current_cases[case_id] = []

        self.current_cases[case_id].append(event)
        pm4pyEventLog = Pm4PyConverter().from_event_log(self.event_log)
        if not case_id in self.models:
            self.models[case_id] = pm4py.discovery.discover_petri_net_inductive(pm4pyEventLog)

        if not case_id in self.models:
            print("Skip")
        else:
            net, im, fm = self.models[case_id]
            alignment = pm4py.conformance.conformance_diagnostics_alignments(
                Pm4PyConverter().from_event_log(self.current_cases[case_id]), net, im, fm
            )[0]
            print(f"Cost: {alignment['cost']}")
            print(f"Visited States: {alignment['visited_states']}")
            print(f"Queued States: {alignment['queued_states']}")