import time
from typing import List

from algorithm.conformance_sink import DistributedConformanceSink
from distributed_environment_builder.infrastructure.network import Network
from process_mining_core.datastructure.core.event import Event

if __name__ == '__main__':
    network: Network = Network("base")

    sink1 = DistributedConformanceSink(["<any>"], name="s1", network=network)
    sink2 = DistributedConformanceSink(["<any>"], name="s2", network=network)

    sinks = {
        "s1": sink1,
        "s2": sink2
    }

    events: List[Event] = [
        Event(case_id="A1", activity="A", timestamp=time.time(), node="s1", group_id="s1"),
        Event(case_id="A1", activity="B", timestamp=time.time(), node="s2", group_id="s1"),
        Event(case_id="A1", activity="C", timestamp=time.time(), node="s2", group_id="s1"),
        Event(case_id="A1", activity="D", timestamp=time.time(), node="s2", group_id="s1"),
        Event(case_id="A2", activity="A", timestamp=time.time(), node="s1", group_id="s1"),
        Event(case_id="A2", activity="B", timestamp=time.time(), node="s2", group_id="s1"),
        Event(case_id="A2", activity="E", timestamp=time.time(), node="s1", group_id="s1")
    ]

    for event in events:
        if event.node in sinks:
            sinks.get(event.node).send(event)

    print(sink1.counted_directly_follows_relations)
    print(sink2.counted_directly_follows_relations)
    print(sink1.start_activity_storage)
    print(sink2.start_activity_storage)
    print(sink1.end_activity_storage.get_counted_end_events())
    print(sink2.end_activity_storage.get_counted_end_events())

