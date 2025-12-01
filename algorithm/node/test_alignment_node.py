import unittest

import pm4py

from algorithm.node.test.distributed_event_log_builder import DistributedEventLogBuilder
from algorithm.petri_net_converter import PetriNetConverter
from algorithm.petri_net_utils import Transition
from process_mining_core.datastructure.core.event import Event


class TestAlignmentNode(unittest.TestCase):

    def init_test_case(self):
        return DistributedEventLogBuilder()

    def init_test_case_central(self):
        return DistributedEventLogBuilder()

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
        env = self.init_test_case()
        node1, node2, node3 = env.three_nodes()
        event = env.eventB("c2")
        env.send(event, "N2")
        print(node2.align_event(event))
        self.assertEqual(1, node2.align_event(event).cost)

    def test_alignment_2_events_1(self):
        env = self.init_test_case()
        node1, node2, node3 = env.three_nodes()
        env.send(env.eventA("c2"), "N1")
        env.send(env.eventB2("c2"), "N2", False)
        env.send(env.eventC("c2"), "N3")

        alignment = node3.align_event(env.eventC("c2"))
        self.assertEqual(2, alignment.cost)
        print(alignment)

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
        event2b = Event(
            timestamp=1,
            activity="B2",
            case_id="c2",
            node="N2",
            group_id=""
        )
        event3 = Event(
            timestamp=1,
            activity="C",
            case_id="c2",
            node="N3",
            group_id=""
        )
        node1.receive_event(event)
        node2.receive_event(event2b, False)
        node3.receive_event(event3)
        alignment = node3.align_event(event3)
        print(alignment)

    def test_alignment_central(self):
        node1 = self.init_test_case_central()
        event = Event(
            timestamp=0,
            activity="A",
            case_id="c2",
            node="N1",
            group_id=""
        )
        event2b = Event(
            timestamp=1,
            activity="B2",
            case_id="c2",
            node="N1",
            group_id=""
        )
        event3 = Event(
            timestamp=1,
            activity="C",
            case_id="c2",
            node="N1",
            group_id=""
        )
        node1.receive_event(event, False)
        node1.receive_event(event2b, False)
        node1.receive_event(event3, False)
        alignment = node1.align_event(event3)
        print(alignment)

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
