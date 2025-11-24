from typing import List


class SinkAssigner:

    def __init__(self, sink_creator):
        self.sink_creator = sink_creator
        self.i = 0

    def assign(self, datasource_ref_list: List[List[str]]):
        sinks = []
        for datasource_refs in datasource_ref_list:
            self.i = self.i + 1
            sinks.append(self.sink_creator(datasource_refs, f"s{self.i}"))
        return sinks