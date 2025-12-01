from process_mining_core.datastructure.core.event import Event


class HiddenEvent:

    def __init__(self, event: Event):
        self.timestamp: str = event.timestamp
        self.activity: str = f"{event.node}({event.activity})"
        self.caseid: str = event.caseid
        self.node: str = event.node
        self.group: str = event.group

