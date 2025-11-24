import unittest

from algorithm.align_path_store import AlignmentStates
from algorithm.align_service import AlignService
from algorithm.fdm import MinimalPetriNet
from algorithm.petri_net_utils import Transition, AlignPath, Marking
from algorithm.testcases.test_petrinet_registry import TestPetriNetRegistry
from distributed_environment_builder.infrastructure.network import Network


class TestAlignmentInternal(unittest.TestCase):

    def test_sync_move_1_activity(self):
        network: Network = Network("base")
        petri_net = TestPetriNetRegistry().get_and_split_petri_net("p1", network)
        self.assertIs(petri_net.align("case1", "A"), 0)

    def test_log_move_end(self):
        network: Network = Network("base")
        petri_net = TestPetriNetRegistry().get_and_split_petri_net("p1", network)
        self.assertIs(petri_net.align("case1", "A"), 0)
        self.assertIs(petri_net.align("case1", "Z"), 1)

    def test_log_move_begin(self):
        network: Network = Network("base")
        petri_net = TestPetriNetRegistry().get_and_split_petri_net("p1", network)
        self.assertIs(petri_net.align("case1", "Z"), 1)
        self.assertIs(petri_net.align("case1", "A"), 1)

    def test_model_move(self):
        network: Network = Network("base")
        petri_net = TestPetriNetRegistry().get_and_split_petri_net("p1", network)
        self.assertIs(petri_net.align("case1", "A"), 0)
        self.assertIs(petri_net.align("case1", "B"), 0)
        self.assertIs(petri_net.align("case1", "D"), 1)

    def test_model_move_2_skips(self):
        network: Network = Network("base")
        petri_net = TestPetriNetRegistry().get_and_split_petri_net("p1", network)
        self.assertIs(petri_net.align("case1", "A"), 0)
        self.assertIs(petri_net.align("case1", "D"), 2)

    def test_and_split_correct_base(self):
        network: Network = Network("base")
        petri_net = TestPetriNetRegistry().get_and_split_petri_net("p1", network)
        self.assertIs(petri_net.align("case1", "A"), 0)
        self.assertIs(petri_net.align("case1", "B"), 0)
        self.assertIs(petri_net.align("case1", "C"), 0)
        self.assertIs(petri_net.align("case1", "D"), 0)

    def test_and_split_correct_flipped(self):
        network: Network = Network("base")
        petri_net = TestPetriNetRegistry().get_and_split_petri_net("p1", network)
        self.assertIs(petri_net.align("case1", "A"), 0)
        self.assertIs(petri_net.align("case1", "C"), 0)
        self.assertIs(petri_net.align("case1", "B"), 0)
        self.assertIs(petri_net.align("case1", "D"), 0)

    def test_case_concurrency(self):
        network: Network = Network("base")
        petri_net = TestPetriNetRegistry().get_and_split_petri_net("p1", network)
        self.assertIs(petri_net.align("case1", "A"), 0)
        self.assertIs(petri_net.align("case1", "C"), 0)
        self.assertIs(petri_net.align("case2", "A"), 0)
        self.assertIs(petri_net.align("case2", "D"), 2)
        self.assertIs(petri_net.align("case1", "D"), 1)

    def test_align_service(self):
        transitions = [
            Transition("A", input_places={"start"}, output_places={"split_b", "split_c"}),
            Transition("B", input_places={"split_b"}, output_places={"join_b"}),
            Transition("C", input_places={"split_c"}, output_places={"join_c"}),
            Transition("D", input_places={"join_b", "join_c"}, output_places={"post_d"})
        ]
        petri_net = MinimalPetriNet(transitions)
        align_service = AlignService()

        align_paths = AlignmentStates()
        align_paths.push_align_path(AlignPath(initial_marking=Marking(place_marking={"start": 1})))
        align_service.calculate_conformance("A", petri_net, align_paths)
        align_service.calculate_conformance("D", petri_net, align_paths)
        align_service.calculate_conformance("B", petri_net, align_paths)
        align_service.calculate_conformance("C", petri_net, align_paths)
        align_service.calculate_conformance("E", petri_net, align_paths)

        while not align_paths.is_empty():
            print(align_paths.pop_align_state())
