from typing import Any, List
from pm4py import discover_petri_net_heuristics

from algorithm.case_time_dict import CaseTimeDict
from algorithm.petri_net_converter import PetriNetConverter
from algorithm.predecessor_utility import PredecessorUtility
from algorithm.service.marking_service import NetworkPredecessor
from algorithm.strategy.discovery.discovery_strategy import DiscoveryStrategy
from process_mining_core.datastructure.core.event import Event

class DiscoveryService:

    def __init__(self, network, node_id, discovery_strategy):
        self.network = network
        self.event_log: List[Event] = []
        self.node_id = node_id
        self.case_time_dict: CaseTimeDict = CaseTimeDict()
        self.petri_net = None
        self.discovery_strategy: DiscoveryStrategy = discovery_strategy

    def learn_event(self, event):
        self.case_time_dict.update_case_with_time(event.caseid, event.timestamp)
        #self.find_predecessor(event)
        self.event_log.append(event)
        pn, im, fm = self.discover()
        self.petri_net = PetriNetConverter().convert(pn, im, fm, node_names=self.network.get_all_node_ids())

    def find_predecessor(self, event):
        network_predecessor = PredecessorUtility().find_predecessor(self.network, event.caseid, self.node_id)
        if self._has_predecessor(network_predecessor, event.caseid):
            self.event_log.append(
                Event(
                    timestamp=network_predecessor.last_timestamp,
                    activity=network_predecessor.node_id,
                    case_id=event.caseid,
                    group_id="",
                    node=""
                )
            )
            network_predecessor.send(self.network).confirm_predecessor(event.caseid, self.node_id, event.timestamp)

    def get_petri_net(self):
        return self.petri_net

    def discover(self):
        return self.discovery_strategy.discover(self.event_log)

    def get_time_for_case(self, case: str) -> str:
        return self.case_time_dict.get_last_time_for_case(case)

    def confirm_predecessor(self, case, node_name, time):
        self.event_log.append(Event(case_id=case, activity=node_name, timestamp=time, node="", group_id=""))

    def get_last_timestamp_of_case(self, case):
        timestamps = [event.timestamp for event in self.event_log if event.caseid == case]
        if not timestamps:
            return None
        return timestamps[-1]

    def _has_predecessor(self, network_predecessor: NetworkPredecessor[Any] | None, case: str) -> bool:
        if not network_predecessor:
            return False

        last_event_of_case = None
        for event in self.event_log:
            if event.caseid == case:
                last_event_of_case = event
        if not last_event_of_case:
            return True
        return network_predecessor.last_timestamp > last_event_of_case.timestamp
