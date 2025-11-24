from typing import List

from pm4py import discover_petri_net_heuristics

from algorithm.strategy.discovery.discovery_strategy import DiscoveryStrategy
from process_mining_core.converter.pm4py_converter import Pm4PyConverter
from process_mining_core.datastructure.core.event import Event

class HeuristicsMinerDiscoveryStrategy(DiscoveryStrategy):

    def discover(self, event_log: List[Event]):
        pm4py_event_log = Pm4PyConverter().from_event_log(event_log)
        return discover_petri_net_heuristics(log=pm4py_event_log)