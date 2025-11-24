class CaseTimeDict:

    def __init__(self):
        self.dict = {}

    def update_case_with_time(self, case, time):
        if not case in self.dict:
            self.dict[case] = time
        else:
            if time > self.dict[case]:
                self.dict[case] = time

    def get_last_time_for_case(self, case):
        if not case in self.dict:
            return None
        return self.dict[case]
