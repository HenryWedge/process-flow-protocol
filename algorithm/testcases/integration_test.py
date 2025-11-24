import time

from algorithm.flow_petri_net import ProcessFlowNode
from distributed_environment_builder.infrastructure.network import Network
from process_mining_core.datastructure.core.event import Event

if __name__ == '__main__':
    network: Network = Network("base")

    ProcessFlowNode("f1", )

    sink1 = ProcessFlowNode(["A", "B", "C", "D"], "s1", network)
    sink2 = ProcessFlowNode(["E", "F", "G"], "s2", network)

    sink1.send(Event(timestamp=time.time(), activity="A", case_id="c1", group_id="G1", node="N1"))
    sink1.send(Event(timestamp=time.time(), activity="B", case_id="c1", group_id="G1", node="N1"))
    sink1.send(Event(timestamp=time.time(), activity="C", case_id="c1", group_id="G1", node="N1"))
    sink1.send(Event(timestamp=time.time(), activity="D", case_id="c1", group_id="G1", node="N1"))

    sink2.send(Event(timestamp=time.time(), activity="E", case_id="c1", group_id="G2", node="N2"))
    sink2.send(Event(timestamp=time.time(), activity="F", case_id="c1", group_id="G2", node="N2"))
    sink2.send(Event(timestamp=time.time(), activity="G", case_id="c1", group_id="G2", node="N2"))

    sink1.conformance(Event(timestamp=time.time(), activity="A", case_id="c2", group_id="G1", node="N1"))
    sink1.conformance(Event(timestamp=time.time(), activity="A", case_id="c1", group_id="G1", node="N1"))
    sink1.conformance(Event(timestamp=time.time(), activity="B", case_id="c2", group_id="G1", node="N1"))
    sink1.conformance(Event(timestamp=time.time(), activity="Y", case_id="c2", group_id="G1", node="N1"))
    sink1.conformance(Event(timestamp=time.time(), activity="D", case_id="c2", group_id="G1", node="N1"))

    sink2.conformance(Event(timestamp=time.time(), activity="E", case_id="c2", group_id="G2", node="N2"))
    sink2.conformance(Event(timestamp=time.time(), activity="F", case_id="c2", group_id="G2", node="N2"))
    sink2.conformance(Event(timestamp=time.time(), activity="G", case_id="c2", group_id="G2", node="N2"))
