from typing import List

from algorithm.node.ground_truth_node import GroundTruthNode
from distributed_event_factory.provider.sink.sink_provider import Sink
from process_mining_core.datastructure.core.event import Event


class GroundTruthSink(Sink):

    def __init__(
            self,
            data_source_ref: List[str],
            node_id,
            network
    ):
        super().__init__(data_source_ref)
        self.node_id = node_id
        self.node: GroundTruthNode = GroundTruthNode(node_id, network)

    def send(self, event: Event) -> None:
        self.node.receive_event(event)

    def get_datasource_ref(self):
        return super().get_datasource_ref()
