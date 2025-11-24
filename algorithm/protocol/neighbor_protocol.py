from abc import ABC, abstractmethod


class NeighborProtocol(ABC):

    @abstractmethod
    def confirm_predecessor(self, case, node_name):
        pass
