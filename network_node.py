from abc import abstractmethod, ABC
from distributed_environment_builder.infrastructure.network import Network

class NetworkNode[T](ABC):

    @abstractmethod
    def __init__(self, node_id: str, network: Network[T]):
        self.node_id = node_id
        self.network: Network[T] = network
        self.network.add_node(self.node_id, self)
