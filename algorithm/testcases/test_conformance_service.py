import unittest

from algorithm.service.conformance_service import ConformanceService


class TestConformanceService(unittest.TestCase):

    def test_silent_transition(self):
        conformance_service = ConformanceService(0)
        conformance_service.calculate_conformance(

        )