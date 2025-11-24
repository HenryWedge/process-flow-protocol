from typing import List

from algorithm.node.process_flow import ProcessFlowNode
from algorithm.strategy.discovery.heuritics_miner_discovery_strategy import HeuristicsMinerDiscoveryStrategy
from distributed_event_factory.provider.sink.sink_provider import Sink
from process_mining_core.datastructure.core.event import Event


class ProcessFlowSink(Sink):
    def __init__(
            self,
            data_source_ref: List[str],
            node_id,
            network
    ):
        super().__init__(data_source_ref)
        self.node_id = node_id
        self.process_flow_node = ProcessFlowNode(node_id, network, HeuristicsMinerDiscoveryStrategy())

    def send(self, event: Event) -> None:
        self.process_flow_node.receive_event_2(event)

    def get_datasource_ref(self):
        return super().get_datasource_ref()

    def get_model(self):
        return self.process_flow_node.discovery_service.discover()

    def get_event_log(self):
        return self.process_flow_node.discovery_service.event_log

    def get_heap_size(self):
        return self.process_flow_node.heap_size()