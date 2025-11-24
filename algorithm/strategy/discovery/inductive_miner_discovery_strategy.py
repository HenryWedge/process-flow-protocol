from typing import List

from algorithm.strategy.discovery.discovery_strategy import DiscoveryStrategy
from process_mining_core.datastructure.core.event import Event


class InductiveMinerDiscoveryStrategy(DiscoveryStrategy):

    def discover(self, event_log: List[Event]):
        pass