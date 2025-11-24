import heapq
import sys
from typing import List, Dict, Set

from algorithm.petri_net_utils import AlignPath, Marking

class AlignmentStates:

    def __init__(self):
        self.store: Dict[str, List[AlignPath]] = {}

    def init_case(self, case, initial_places: Set[str]):
        paths = []
        for place in initial_places:
            paths.append(AlignPath(Marking({place: 1})))
        self.store[case] = paths

    def mark_place(self, case, place):
        if not case in self.store:
            self.store[case] = [AlignPath(Marking({}))]
        for path in self.store[case]:
            path.mark_place(place)
            #path.add_input_cost(cost)

    def push_align_path(self, case, align_path: AlignPath):
        if not case in self.store:
            self.store[case] = [AlignPath(Marking({}))]
        heapq.heappush(self.store[case], align_path)

    def pop_align_state(self, case) -> AlignPath:
        return heapq.heappop(self.store[case])

    def get_minimal_cost(self, case):
        if self.store[case]:
            return self.top(case).cost()
        return sys.maxsize

    def top(self, case):
        return heapq.nsmallest(1, self.store[case])[0]

    def is_empty(self, case):
        if not case in self.store:
            return True
        return self.store[case] == []

    def size(self):
        return len(self.store)

    def size_of_case(self, case):
        return len(self.store[case])