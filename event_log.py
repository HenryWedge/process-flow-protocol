from typing import List

from process_mining_core.datastructure.core.event import Event

class Trace:

    def __init__(self):
        self.activities = []

    def append_activity(self, activity):
        self.activities.append(activity)

    def __hash__(self):
        return hash(str(self.activities))

    def __eq__(self, other):
        return self.activities == other.activities

    def __str__(self):
        return str(self.activities)

class EventLog:
    def __init__(self, events: List[Event]):
        self.events = events

    def get_variants(self):
        traces= {}
        variants = {}
        for event in self.events:
            if not event.caseid in traces:
                traces[event.caseid] = Trace()
            traces[event.caseid].append_activity(event.activity)

        for trace in traces:
            if traces[trace] not in variants:
                variants[traces[trace]] = 0
            variants[traces[trace]] = variants[traces[trace]] + 1
        return variants