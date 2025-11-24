import time
import unittest

from algorithm.protocol.conformance_protocol import ConformanceProtocol
from algorithm.node.process_flow import ProcessFlowNode
from algorithm.strategy.discovery.heuritics_miner_discovery_strategy import HeuristicsMinerDiscoveryStrategy
from distributed_environment_builder.infrastructure.network import Network
from process_mining_core.datastructure.core.event import Event


class MarkingServiceTest(unittest.TestCase):

    def test_simple(self):
        network: Network[ConformanceProtocol] = Network("marking")
        petri_net_1 = ProcessFlowNode(
            node_id="p1",
            network=network,
            discovery_strategy=HeuristicsMinerDiscoveryStrategy()
        )

        petri_net_2 = ProcessFlowNode(
            node_id="p2",
            network=network,
            discovery_strategy=HeuristicsMinerDiscoveryStrategy()
        )

        network.add_node("p1", petri_net_1)
        network.add_node("p2", petri_net_2)

        petri_net_1.receive_event(Event(case_id="case1", activity="A", timestamp=time.time() + 10, group_id="", node=""))
        petri_net_1.receive_event(Event(case_id="case1", activity="B", timestamp=time.time() + 20, group_id="", node=""))
        petri_net_1.receive_event(Event(case_id="case1", activity="C", timestamp=time.time() + 30, group_id="", node=""))
        petri_net_2.receive_event(Event(case_id="case1", activity="D", timestamp=time.time() + 40, group_id="", node=""))
        petri_net_2.receive_event(Event(case_id="case1", activity="F", timestamp=time.time() + 50, group_id="", node=""))
        petri_net_2.receive_event(Event(case_id="case1", activity="G", timestamp=time.time() + 60, group_id="", node=""))

        petri_net_1.receive_event(Event(case_id="case2", activity="A", timestamp=time.time()+70, group_id="", node=""))
        petri_net_1.receive_event(Event(case_id="case2", activity="B", timestamp=time.time()+80, group_id="", node=""))
        #petri_net_1.receive_event(Event(case_id="case2", activity="E", timestamp=time.time()+90, group_id="", node=""))
        petri_net_2.receive_event(Event(case_id="case2", activity="D", timestamp=time.time()+100, group_id="", node=""))
        petri_net_2.receive_event(Event(case_id="case2", activity="G", timestamp=time.time()+110, group_id="", node=""))
        print(network.send_count)
        print(petri_net_1.heap_size())
        print(petri_net_2.heap_size())



