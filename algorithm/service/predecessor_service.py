from algorithm.network_predecessor import NetworkPredecessor
from algorithm.predecessor_utility import PredecessorUtility
from algorithm.protocol.conformance_protocol import ConformanceProtocol
from distributed_environment_builder.infrastructure.network import Network
from process_mining_core.datastructure.core.event import Event


class PredecessorService:

    def __init__(self, network: Network[ConformanceProtocol]):
        self.network: Network[ConformanceProtocol] = network

    def find_predecessor_event(self, case, own_id, last_timestamp):
        # Consider multiple predecessors
        network_predecessor: NetworkPredecessor = PredecessorUtility().find_predecessor(self.network, case=case, own_id=own_id)
        if not network_predecessor or (last_timestamp and last_timestamp > network_predecessor.last_timestamp):
            return None
        else:
            return Event(
                case_id=case,
                activity=network_predecessor.node_id,
                timestamp=network_predecessor.last_timestamp,
                node="",
                group_id=""
            )

