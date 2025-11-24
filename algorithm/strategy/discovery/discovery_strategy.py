from abc import abstractmethod, ABC
from typing import List

from process_mining_core.datastructure.core.event import Event

class DiscoveryStrategy(ABC):

    @abstractmethod
    def discover(self, event_log: List[Event]):
        pass