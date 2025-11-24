from algorithm.distributed_alignment import DistributedPetriNet
from algorithm.petri_net_utils import ReceivingPlace, Transition
from distributed_environment_builder.infrastructure.network import Network


class TestPetriNetRegistry:

    def get_and_split_petri_net(self, node_id: str, network: Network):
        return DistributedPetriNet(
            node_id="node_id",
            receiving_place={
                ReceivingPlace("start", "")
            },
            places={"start", "split_b", "split_c", "join", "post_d"},
            transitions={
                Transition("A", input_places={"start"}, output_places={"split_b", "split_c"}),
                Transition("B", input_places={"split_b"}, output_places={"join_b"}),
                Transition("C", input_places={"split_c"}, output_places={"join_c"}),
                Transition("D", input_places={"join_b", "join_c"}, output_places={"post_d"}),
            },
            initial_places={"start"},
            final_places={"post_d"},
            network=network
        )

    def get_and_split_petri_net_xor(self, node_id: str, network: Network):
        return DistributedPetriNet(
            node_id="node_id",
            receiving_place={
                ReceivingPlace("start", "")
            },
            places={"start", "split_b", "split_c", "join", "post_d"},
            transitions={
                Transition("A", input_places={"start"}, output_places={"split_b", "split_c"}),
                Transition("B", input_places={"split_b"}, output_places={"join_b"}),
                Transition("C", input_places={"split_c"}, output_places={"post_c"}),
                Transition("D", input_places={"post_c"}, output_places={"post_d"}),
                Transition("E", input_places={"join_b"}, output_places={"post_e"}),
                Transition("E", input_places={"post_d"}, output_places={"post_e"}),
            },
            initial_places={"start"},
            final_places={"post_d"},
            network=network
        )