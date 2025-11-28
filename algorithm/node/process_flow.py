from algorithm.service.conformance_service import ConformanceService
from algorithm.protocol.conformance_protocol import ConformanceProtocol
from algorithm.service.discovery_service import DiscoveryService
from algorithm.service.marking_service import MarkingService
from algorithm.protocol.neighbor_protocol import NeighborProtocol
from algorithm.service.predecessor_service import PredecessorService
from algorithm.strategy.discovery.discovery_strategy import DiscoveryStrategy
from distributed_environment_builder.infrastructure.network import Network
from network_node import NetworkNode
from process_mining_core.datastructure.core.event import Event

class ProcessFlowNode(NetworkNode, ConformanceProtocol, NeighborProtocol):

    def __init__(
            self,
            node_id: str,
            network: Network[ConformanceProtocol],
            discovery_strategy: DiscoveryStrategy
    ):
        super().__init__(node_id, network)
        self.marking_service = MarkingService(network)
        self.conformance_service = ConformanceService(network, 2, node_id)
        self.discovery_service = DiscoveryService(network, self.node_id, discovery_strategy)
        self.predecessor_service = PredecessorService(self.network)
        self.petri_nets = {}

    def receive_event(self, event: Event):
        self.learn_event(event)
        self.alignment(event)

    def process_event(self, event: Event):
        predecessor_events = self.predecessor_service.find_predecessor_events(
            case=event.caseid, own_id=self.node_id,
            last_timestamp=self.discovery_service.get_last_timestamp_of_case(
                case=event.caseid
            )
        )
        for predecessor_event in predecessor_events:
            if predecessor_event:
                self.learn_event(predecessor_event)
        self.learn_event(event)
        for predecessor_event in predecessor_events:
            if predecessor_event:
                cost = self.alignment(predecessor_event)
                print(f"Minimal cost: {cost}")
                print("------------")
        cost = self.alignment(event)
        print(f"Minimal cost: {cost}")
        print("------------")
        return cost

    def learn_event(self, event: Event) -> None:
        self.discovery_service.learn_event(event)

    def get_time_for_case(self, case: str) -> str:
        return self.discovery_service.get_time_for_case(case)

    def confirm_predecessor(self, case, node_name, time):
        self.discovery_service.confirm_predecessor(case, node_name, time)

    def update_marking(self, event):
        self.marking_service.update_marking(
            event,
            self.discovery_service.get_petri_net(),
            self.conformance_service.get_alignment_states()
        )

    def alignment(self, event):
        print(f"Activity: {event.activity}")
        if not event.caseid in self.petri_nets:
            self.petri_nets[event.caseid] = self.discovery_service.get_petri_net()

        self.conformance_service.calculate_conformance(
            petri_net=self.petri_nets[event.caseid],
            case=event.caseid,
            activity=event.activity
        )
        if event.caseid in self.conformance_service.alignment_states.store:
            for align_path in self.conformance_service.alignment_states.store[event.caseid]:
                print(align_path)

        return self.conformance_service.alignment_states.top(event.caseid).cost()

    def get_conformance_for_case(self, case) -> int:
        return self.conformance_service.get_conformance_for_case(case)

    def get_conformance_to_end_for_case(self, case, target_node) -> int:
        if not case in self.petri_nets:
            return 0
        return self.conformance_service.get_conformance_to_end_for_case(case, self.petri_nets[case], target_node=target_node)

    def heap_size(self):
        return self.conformance_service.get_alignment_states()
