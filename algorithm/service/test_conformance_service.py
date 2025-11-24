from tensorflow_datasets.core.units_test import UnitsTest

from algorithm.petri_net import DistributedPetriNet
from algorithm.petri_net_utils import Transition
from algorithm.service.conformance_service import ConformanceService


class TestConformanceService(UnitsTest):

    def test_conformance(self):
        conformance_service = ConformanceService(0)

        alignment_states = conformance_service.calculate_conformance(
            case="c1",
            activity="C",
            petri_net=DistributedPetriNet(
                transitions=[
                    Transition(
                        activity_label="A",
                        input_places={"b_A"},
                        output_places={"a_A"}
                    ),
                    Transition(
                        activity_label="B",
                        input_places={"a_A"},
                        output_places={"a_B"}
                    ),
                    Transition(
                        activity_label="C",
                        input_places={"a_B"},
                        output_places={"a_C"}
                    )
                ],
                initial_places={"b_A"},
                inbound_places=[],
                outbound_places=[]
            )
        )
        print(alignment_states)
