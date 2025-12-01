from algorithm.node.alignment_node import AlignmentNode
from distributed_environment_builder.infrastructure.network import Network
from process_mining_core.datastructure.core.event import Event


class DistributedEventLogBuilder:

    def __init__(self):
        self.network: Network = Network("base")
        self.node1 = AlignmentNode("N1", self.network)
        self.node2 = AlignmentNode("N2", self.network)
        self.node3 = AlignmentNode("N3", self.network)

    def decentral_topology(self):
        return {
            "N1": self.node1,
            "N2": self.node2,
            "N3": self.node3
        }

    def three_nodes(self):
        self.send(self.eventA(), "N1")
        self.send(self.eventB(), "N2")
        self.send(self.eventC(), "N3")
        self.send(self.eventD(), "N1")
        self.send(self.eventE(), "N2")
        top = self.decentral_topology()
        return self.node1, self.node2, self.node3

    def three_events_central(self):
        self.send(self.eventA(), "N1")
        self.send(self.eventB(), "N1")
        self.send(self.eventC(), "N1")
        self.send(self.eventD(), "N1")
        self.send(self.eventE(), "N1")
        top = self.decentral_topology()
        return top["N1"], top["N2"], top["N3"]

    def send(self, event: Event, location: str, learn=True):
        event.node = location
        self.decentral_topology()[location].receive_event(event, learn)

    def eventA(self, case="c1"):
        return Event(
            timestamp=0,
            activity="A",
            case_id=case,
            node="N1",
            group_id=""
        )

    def eventB(self, case="c1"):
        return Event(
            timestamp=0,
            activity="B",
            case_id=case,
            node="N2",
            group_id=""
        )

    def eventB2(self, case="c1"):
        return Event(
            timestamp=0,
            activity="B2",
            case_id=case,
            node="N2",
            group_id=""
        )

    def eventC(self, case="c1"):
        return Event(
            timestamp=0,
            activity="C",
            case_id=case,
            node="N3",
            group_id=""
        )

    def eventD(self):
        return Event(
            timestamp=0,
            activity="D",
            case_id="c1",
            node="N1",
            group_id=""
        )

    def eventE(self):
        return Event(
            timestamp=0,
            activity="E",
            case_id="c1",
            node="N2",
            group_id=""
        )
