from distributed_environment_builder.infrastructure.network import Network


class NetworkPredecessor[T]:
    def __init__(self, node_id, last_timestamp: str = ""):
        self.node_id = node_id
        self.last_timestamp = last_timestamp

    def update_last_timestamp(self, last_timestamp):
        self.last_timestamp = last_timestamp

    def send(self, network: Network[T]) -> T:
        return network.get_node(self.node_id)

    def __lt__(self, other):
        return self.last_timestamp < other.last_timestamp
