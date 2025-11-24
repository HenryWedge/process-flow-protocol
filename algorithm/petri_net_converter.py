from typing import List

from algorithm.petri_net import DistributedPetriNet
from algorithm.petri_net_utils import Transition, ReceivingPlace
from pm4py.objects.petri_net.obj import PetriNet, Marking

class PetriNetConverter:

    def convert(
        self,
        petri_net: PetriNet,
        initial_marking: Marking,
        final_marking: Marking,
        node_names: List[str]
    ) -> DistributedPetriNet:

        places = []
        for place in petri_net.places:
            places.append(place)

        transitions = []
        inbound_places = []
        outbound_places = []
        for transition in petri_net.transitions:
            label = transition.label
            input_places = []
            output_places = []

            for in_arc in transition.in_arcs:
                input_places.append(in_arc.source.name)

            for out_arc in transition.out_arcs:
                output_places.append(out_arc.target.name)

            if label in node_names:
                if label in [arc.target.label for arc in transition.in_arcs]:
                    inbound_places.append(label)
                if label in [arc.source.label for arc in transition.out_arcs]:
                    outbound_places.append(label)

            transitions.append(
                Transition(
                    activity_label=label,
                    input_places=input_places,
                    output_places=output_places
                )
            )

        initial_places = []
        for im in initial_marking:
            initial_places.append(im.name)

        final_places = []
        for fm in final_marking:
            final_places.append(fm.name)

        return DistributedPetriNet(
            transitions=transitions,
            initial_places=initial_places,
            inbound_places=inbound_places,
            outbound_places=outbound_places
        )
