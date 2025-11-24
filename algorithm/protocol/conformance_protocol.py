from abc import abstractmethod, ABC


class ConformanceProtocol(ABC):

    @abstractmethod
    def get_time_for_case(self, case) -> str:
        pass

    @abstractmethod
    def get_conformance_for_case(self, case) -> int:
        pass

    @abstractmethod
    def get_conformance_to_end_for_case(self, case, target_node_id) -> int:
        pass

    @abstractmethod
    def confirm_predecessor(self, case, node_name, time):
        pass

