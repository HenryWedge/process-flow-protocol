import unittest

from algorithm.petri_net_utils import Marking
from algorithm.testcases.test_petrinet_registry import TestPetriNetRegistry
from distributed_environment_builder.infrastructure.network import Network


class TestFindShortestWayToActivityMove(unittest.TestCase):

    def test_shortest_way_1(self):
        network: Network = Network("base")
        petri_net = TestPetriNetRegistry().get_and_split_petri_net("p1", network)
        self.assertIs(petri_net.find_shortest_way_to_activity_move(marking=Marking(place_marking={"start": 1}), current_place="split_b" , cost=0), 1)

    def test_shortest_way_2(self):
        network: Network = Network("base")
        petri_net = TestPetriNetRegistry().get_and_split_petri_net("p1", network)
        self.assertIs(petri_net.find_shortest_way_to_activity_move(marking=Marking(place_marking={"start": 1}), current_place="post_d" , cost=0), 3)

    def test_shortest_way_start_in_middle(self):
        network: Network = Network("base")
        petri_net = TestPetriNetRegistry().get_and_split_petri_net("p1", network)
        self.assertIs(petri_net.find_shortest_way_to_activity_move(marking=Marking(place_marking={"join_c": 1, "join_b": 1}), current_place="post_d" , cost=0), 1)

    def test_shortest_way_start_in_middle_2(self):
        network: Network = Network("base")
        petri_net = TestPetriNetRegistry().get_and_split_petri_net("p1", network)
        self.assertIs(petri_net.find_shortest_way_to_activity_move(marking=Marking(place_marking={"split_c": 1, "join_b": 1}), current_place="post_d" , cost=0), 2)