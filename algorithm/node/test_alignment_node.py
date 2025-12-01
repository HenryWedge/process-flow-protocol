import unittest

import pm4py

from algorithm.node.alignment_node import AlignmentNode
from algorithm.petri_net_converter import PetriNetConverter
from algorithm.petri_net_utils import Transition
from distributed_environment_builder.infrastructure.network import Network
from process_mining_core.datastructure.core.event import Event


class TestAlignmentNode(unittest.TestCase):

    def init_test_case(self):
        network: Network = Network("base")
        node1 = AlignmentNode("N1", network)
        node2 = AlignmentNode("N2", network)
        node3 = AlignmentNode("N3", network)

        node1.receive_event(event=Event(
            timestamp=0,
            activity="A",
            case_id="c1",
            node="N1",
            group_id=""
        ))

        node2.receive_event(event=Event(
            timestamp=0,
            activity="B",
            case_id="c1",
            node="N2",
            group_id=""
        ))

        node3.receive_event(event=Event(
            timestamp=0,
            activity="C",
            case_id="c1",
            node="N3",
            group_id=""
        ))

        node1.receive_event(event=Event(
            timestamp=0,
            activity="D",
            case_id="c1",
            node="N1",
            group_id=""
        ))

        node2.receive_event(event=Event(
            timestamp=0,
            activity="E",
            case_id="c1",
            node="N2",
            group_id=""
        ))

        return node1, node2, node3

    def test_collect_event_log_correctly(self):
        node1, node2, node3 = self.init_test_case()
        self.assertListEqual([event.activity for event in node1.global_event_log["c1"]],
                             ['N1(A)', 'N2(B)', 'N3(C)', 'N1(D)'])
        self.assertListEqual([event.activity for event in node2.global_event_log["c1"]],
                             ['N1(A)', 'N2(B)', 'N3(C)', 'N1(D)', 'N2(E)'])
        self.assertListEqual([event.activity for event in node3.global_event_log["c1"]], ['N1(A)', 'N2(B)', 'N3(C)'])

    def test_show_event_log(self):
        node1, node2, node3 = self.init_test_case()
        pn, im, fm = node2.model, node2.im, node2.fm
        view = pm4py.visualization.petri_net.visualizer.apply(pn, im, fm)
        pm4py.visualization.petri_net.visualizer.view(view)

    def test_alignment_path(self):
        node1, node2, node3 = self.init_test_case()
        pn, im, fm = node2.model, node2.im, node2.fm
        petri_net = PetriNetConverter().convert(pn, im, fm, [])
        print([transition.activity_label for transition in
               node2.bfs_shortest_path_between_activities_reverse(petri_net, "N2(E)", "N1(D)")])

    def test_alignment_start_event(self):
        node1, node2, node3 = self.init_test_case()
        event = Event(
            timestamp=0,
            activity="A",
            case_id="c2",
            node="N1",
            group_id=""
        )
        node1.receive_event(event)
        self.assertEqual(0, node1.align_event(event).cost)

    def test_skip_start_event(self):
        node1, node2, node3 = self.init_test_case()
        event = Event(
            timestamp=0,
            activity="B",
            case_id="c2",
            node="N2",
            group_id=""
        )
        node2.receive_event(event)
        print(node2.align_event(event))
        #self.assertEqual(1, node2.align_event(event).cost)

    def test_alignment_2_events(self):
        node1, node2, node3 = self.init_test_case()
        event = Event(
            timestamp=0,
            activity="A",
            case_id="c2",
            node="N1",
            group_id=""
        )
        event2 = Event(
            timestamp=1,
            activity="B",
            case_id="c2",
            node="N2",
            group_id=""
        )
        node1.receive_event(event)
        self.assertEqual(0, node1.align_event(event).cost)
        node2.receive_event(event2)
        self.assertEqual(0, node2.align_event(event2).cost)

    def test_alignment_skip_start_event_2_nodes(self):
        node1, node2, node3 = self.init_test_case()
        event2 = Event(
            timestamp=0,
            activity="B",
            case_id="c2",
            node="N2",
            group_id=""
        )
        node2.receive_event(event2)
        self.assertEqual(1, node2.align_event(event2).cost)

    def test_calculate_alignment(self):
        node1, node2, node3 = self.init_test_case()
        print(node1.calculate_alignment(
            [
                Transition(activity_label="A", input_places={}, output_places={}),
                Transition(activity_label="B", input_places={}, output_places={}),
                Transition(activity_label="C", input_places={}, output_places={}),
                Transition(activity_label="D", input_places={}, output_places={}),
            ],
            [
                Event(activity="A", case_id="", timestamp="", node="", group_id=""),
                Event(activity="B", case_id="", timestamp="", node="", group_id=""),
                Event(activity="C", case_id="", timestamp="", node="", group_id=""),
                Event(activity="D", case_id="", timestamp="", node="", group_id=""),
            ]
        ))