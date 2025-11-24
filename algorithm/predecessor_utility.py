from algorithm.protocol.conformance_protocol import ConformanceProtocol
from algorithm.service.marking_service import NetworkPredecessor
from distributed_environment_builder.infrastructure.network import Network

class PredecessorUtility:

    def find_predecessor(self, network: Network[ConformanceProtocol], case: str, own_id: str):
        largest_time = None
        predecessor = None
        for node in network.get_all_nodes(own_id):
            time = node.get_time_for_case(case)
            if time and (not largest_time or time >= largest_time):
                largest_time = time
                predecessor = node
        if not predecessor:
            return None
        return NetworkPredecessor(predecessor.node_id, largest_time)