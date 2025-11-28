import unittest

import pm4py

from algorithm.node.process_flow import ProcessFlowNode
from algorithm.strategy.discovery.heuritics_miner_discovery_strategy import HeuristicsMinerDiscoveryStrategy
from distributed_environment_builder.infrastructure.network import Network
from process_mining_core.datastructure.core.event import Event

network = Network("base")
network2 = Network("base")
node1 = ProcessFlowNode("s1", network, HeuristicsMinerDiscoveryStrategy())
node2 = ProcessFlowNode("s2", network, HeuristicsMinerDiscoveryStrategy())
node3 = ProcessFlowNode("s3", network, HeuristicsMinerDiscoveryStrategy())
central_node = ProcessFlowNode("s4", network2, HeuristicsMinerDiscoveryStrategy())


class SepsisTest(unittest.TestCase):

    def build_event(self, case, activity, timestamp):
        return Event(
            case_id=case,
            activity=activity,
            timestamp=timestamp,
            node="",
            group_id=""
        )

    def assign(self, event):
        if event.activity in ["CRP", "Release B", "Release A", "Release D", "Release C", "Release E"]:
            cost = node1.process_event(event)
        elif event.activity in ["Admission IC", "Return ER", "ER Triage", "IV Antibiotics", "Leucocytes",
                                "ER Registration"]:
            cost = node2.process_event(event)
        elif event.activity in ["IV Liquid", "Admission NC", "LacticAcid", "ER Sepsis Triage"]:
            cost = node3.process_event(event)
        print(f"Minimal cost: {cost}")
        print("------------")
        return cost

    def test_central(self):
        central_node.process_event(self.build_event("case1", activity="ER Registration", timestamp="2014-10-22T11:15:41.000+02:00"))
        central_node.process_event(self.build_event("case1", activity="Leucocytes", timestamp="2014-10-22T11:27:00.000+02:00"))
        central_node.process_event(self.build_event("case1", activity="CRP", timestamp="2014-10-22T11:27:00.000+02:00"))
        central_node.process_event(self.build_event("case1", activity="LacticAcid", timestamp="2014-10-22T11:27:00.000+02:00"))
        central_node.process_event(self.build_event("case1", activity="ER Triage", timestamp="2014-10-22T11:33:37.000+02:00"))
        central_node.process_event(self.build_event("case1", activity="ER Sepsis Triage", timestamp="2014-10-22T11:34:00.000+02:00"))
        central_node.process_event(self.build_event("case1", activity="IV Liquid", timestamp="2014-10-22T14:03:47.000+02:00"))
        central_node.process_event(self.build_event("case1", activity="IV Antibiotics", timestamp="2014-10-22T14:03:47.000+02:00"))
        central_node.process_event(self.build_event("case1", activity="Admission NC", timestamp="2014-10-22T14:13:19.000+02:00"))
        central_node.process_event(self.build_event("case1", activity="CRP", timestamp="2014-10-24T09:00:00.000+02:00"))
        central_node.process_event(self.build_event("case1", activity="Leucocytes", timestamp="2014-10-24T09:00:00.000+02:00"))
        central_node.process_event(self.build_event("case1", activity="Leucocytes", timestamp="2014-10-26T08:00:00.000+01:00"))
        central_node.process_event(self.build_event("case1", activity="CRP", timestamp="2014-10-26T08:00:00.000+01:00"))
        central_node.process_event(self.build_event("case1", activity="Leucocytes", timestamp="2014-10-28T08:00:00.000+01:00"))
        central_node.process_event(self.build_event("case1", activity="CRP", timestamp="2014-10-28T08:00:00.000+01:00"))
        central_node.process_event(self.build_event("case1", activity="CRP", timestamp="2014-10-30T08:00:00.000+01:00"))
        central_node.process_event(self.build_event("case1", activity="Leucocytes", timestamp="2014-10-30T08:00:00.000+01:00"))
        central_node.process_event(self.build_event("case1", activity="Leucocytes", timestamp="2014-10-31T08:00:00.000+01:00"))
        central_node.process_event(self.build_event("case1", activity="CRP", timestamp="2014-10-31T08:00:00.000+01:00"))
        central_node.process_event(self.build_event("case1", activity="CRP", timestamp="2014-11-02T08:00:00.000+01:00"))
        central_node.process_event(self.build_event("case1", activity="Leucocytes", timestamp="2014-11-02T08:00:00.000+01:00"))
        central_node.process_event(self.build_event("case1", activity="Release A", timestamp="2014-11-02T15:15:00.000+01:00"))

        central_node.process_event(self.build_event("case2", activity="ER Registration", timestamp="2014-12-21T11:04:24.000+01:00"))
        central_node.process_event(self.build_event("case2", activity="ER Triage", timestamp="2014-12-21T11:17:19.000+01:00"))
        central_node.process_event(self.build_event("case2", activity="CRP", timestamp="2014-12-21T11:36:00.000+01:00"))
        central_node.process_event(self.build_event("case2", activity="LacticAcid", timestamp="2014-12-21T11:36:00.000+01:00"))
        central_node.process_event(self.build_event("case2", activity="Leucocytes", timestamp="2014-12-21T11:36:00.000+01:00"))
        central_node.process_event(self.build_event("case2", activity="ER Sepsis Triage", timestamp="2014-12-21T12:15:45.000+01:00"))
        central_node.process_event(self.build_event("case2", activity="IV Liquid", timestamp="2014-12-21T12:33:48.000+01:00"))
        central_node.process_event(self.build_event("case2", activity="IV Antibiotics", timestamp="2014-12-21T12:33:55.000+01:00"))
        central_node.process_event(self.build_event("case2", activity="Admission NC", timestamp="2014-12-21T13:17:08.000+01:00"))
        central_node.process_event(self.build_event("case2", activity="CRP", timestamp="2014-12-24T08:00:00.000+01:00"))
        central_node.process_event(self.build_event("case2", activity="CRP", timestamp="2014-12-26T14:00:00.000+01:00"))
        central_node.process_event(self.build_event("case2", activity="Release A", timestamp="2014-12-26T18:00:00.000+01:00"))

        pn, im, fm = central_node.discovery_service.discover()
        view = pm4py.visualization.petri_net.visualizer.apply(pn, im, fm)
        pm4py.visualization.petri_net.visualizer.view(view)

        self.assertEqual(
            0, central_node.process_event(
                self.build_event("case3", activity="ER Registration", timestamp="2014-02-09T19:29:29.000+01:00")))

        self.assertEqual(
            0, central_node.process_event(self.build_event("case3", activity="ER Triage", timestamp="2014-02-09T20:05:23.000+01:00")))

        self.assertEqual(
            0,
                central_node.process_event(self.build_event("case3", activity="ER Sepsis Triage", timestamp="2014-02-09T20:05:33.000+01:00")))
        self.assertEqual(
            1,
            central_node.process_event(self.build_event("case3", activity="Leucocytes", timestamp="2014-02-09T20:06:00.000+01:00")))
        self.assertEqual(
            1,
            central_node.process_event(self.build_event("case3", activity="CRP", timestamp="2014-02-09T20:06:00.000+01:00")))



    def test_first_events_of_sepsis(self):
        self.assign(self.build_event("case1", activity="ER Registration", timestamp="2014-10-22T11:15:41.000+02:00"))
        self.assign(self.build_event("case1", activity="Leucocytes", timestamp="2014-10-22T11:27:00.000+02:00"))
        self.assign(self.build_event("case1", activity="CRP", timestamp="2014-10-22T11:27:00.000+02:00"))
        self.assign(self.build_event("case1", activity="LacticAcid", timestamp="2014-10-22T11:27:00.000+02:00"))
        self.assign(self.build_event("case1", activity="ER Triage", timestamp="2014-10-22T11:33:37.000+02:00"))
        self.assign(self.build_event("case1", activity="ER Sepsis Triage", timestamp="2014-10-22T11:34:00.000+02:00"))
        self.assign(self.build_event("case1", activity="IV Liquid", timestamp="2014-10-22T14:03:47.000+02:00"))
        self.assign(self.build_event("case1", activity="IV Antibiotics", timestamp="2014-10-22T14:03:47.000+02:00"))
        self.assign(self.build_event("case1", activity="Admission NC", timestamp="2014-10-22T14:13:19.000+02:00"))
        self.assign(self.build_event("case1", activity="CRP", timestamp="2014-10-24T09:00:00.000+02:00"))
        self.assign(self.build_event("case1", activity="Leucocytes", timestamp="2014-10-24T09:00:00.000+02:00"))
        self.assign(self.build_event("case1", activity="Leucocytes", timestamp="2014-10-26T08:00:00.000+01:00"))
        self.assign(self.build_event("case1", activity="CRP", timestamp="2014-10-26T08:00:00.000+01:00"))
        self.assign(self.build_event("case1", activity="Leucocytes", timestamp="2014-10-28T08:00:00.000+01:00"))
        self.assign(self.build_event("case1", activity="CRP", timestamp="2014-10-28T08:00:00.000+01:00"))
        self.assign(self.build_event("case1", activity="CRP", timestamp="2014-10-30T08:00:00.000+01:00"))
        self.assign(self.build_event("case1", activity="Leucocytes", timestamp="2014-10-30T08:00:00.000+01:00"))
        self.assign(self.build_event("case1", activity="Leucocytes", timestamp="2014-10-31T08:00:00.000+01:00"))
        self.assign(self.build_event("case1", activity="CRP", timestamp="2014-10-31T08:00:00.000+01:00"))
        self.assign(self.build_event("case1", activity="CRP", timestamp="2014-11-02T08:00:00.000+01:00"))
        self.assign(self.build_event("case1", activity="Leucocytes", timestamp="2014-11-02T08:00:00.000+01:00"))
        self.assign(self.build_event("case1", activity="Release A", timestamp="2014-11-02T15:15:00.000+01:00"))

        self.assign(self.build_event("case2", activity="ER Registration", timestamp="2014-12-21T11:04:24.000+01:00"))
        self.assign(self.build_event("case2", activity="ER Triage", timestamp="2014-12-21T11:17:19.000+01:00"))
        self.assign(self.build_event("case2", activity="CRP", timestamp="2014-12-21T11:36:00.000+01:00"))
        self.assign(self.build_event("case2", activity="LacticAcid", timestamp="2014-12-21T11:36:00.000+01:00"))
        self.assign(self.build_event("case2", activity="Leucocytes", timestamp="2014-12-21T11:36:00.000+01:00"))
        self.assign(self.build_event("case2", activity="ER Sepsis Triage", timestamp="2014-12-21T12:15:45.000+01:00"))
        self.assign(self.build_event("case2", activity="IV Liquid", timestamp="2014-12-21T12:33:48.000+01:00"))
        self.assign(self.build_event("case2", activity="IV Antibiotics", timestamp="2014-12-21T12:33:55.000+01:00"))
        self.assign(self.build_event("case2", activity="Admission NC", timestamp="2014-12-21T13:17:08.000+01:00"))
        self.assign(self.build_event("case2", activity="CRP", timestamp="2014-12-24T08:00:00.000+01:00"))
        self.assign(self.build_event("case2", activity="CRP", timestamp="2014-12-26T14:00:00.000+01:00"))
        self.assign(self.build_event("case2", activity="Release A", timestamp="2014-12-26T18:00:00.000+01:00"))

        pn, im, fm = node1.discovery_service.discover()
        #pn2, im2, fm2 = node2.discovery_service.discover()
        #pn3, im3, fm3 = node3.discovery_service.discover()
        view = pm4py.visualization.petri_net.visualizer.apply(pn, im, fm)
        #view2 = pm4py.visualization.petri_net.visualizer.apply(pn2, im2, fm2)
        #view3 = pm4py.visualization.petri_net.visualizer.apply(pn3, im3, fm3)
        pm4py.visualization.petri_net.visualizer.view(view)
        #pm4py.visualization.petri_net.visualizer.view(view2)
        #pm4py.visualization.petri_net.visualizer.view(view3)

        self.assertEqual(
            0, self.assign(
                self.build_event("case3", activity="ER Registration", timestamp="2014-02-09T19:29:29.000+01:00")))

        self.assertEqual(
            0, self.assign(self.build_event("case3", activity="ER Triage", timestamp="2014-02-09T20:05:23.000+01:00")))

        self.assertEqual(
            0,
            self.assign(self.build_event("case3", activity="ER Sepsis Triage", timestamp="2014-02-09T20:05:33.000+01:00")))
        self.assertEqual(
            1,
            self.assign(self.build_event("case3", activity="Leucocytes", timestamp="2014-02-09T20:06:00.000+01:00")))
        self.assertEqual(
            1,
            self.assign(self.build_event("case3", activity="CRP", timestamp="2014-02-09T20:06:00.000+01:00")))
        # self.assign(self.build_event("case3", activity="IV Liquid", timestamp="2014-02-09T20:07:12.000+01:00"))
        # self.assign(self.build_event("case3", activity="IV Antibiotics", timestamp="2014-02-09T20:07:19.000+01:00"))
        # self.assign(self.build_event("case3", activity="Admission NC", timestamp="2014-02-09T22:53:46.000+01:00"))
        # self.assign(self.build_event("case3", activity="Admission NC", timestamp="2014-02-11T08:14:11.000+01:00"))
        # self.assign(self.build_event("case3", activity="Leucocytes", timestamp="2014-02-11T08:57:00.000+01:00"))
        # self.assign(self.build_event("case3", activity="CRP", timestamp="2014-02-11T08:57:00.000+01:00"))
        # self.assign(self.build_event("case3", activity="Leucocytes", timestamp="2014-02-14T08:00:00.000+01:00"))
        # self.assign(self.build_event("case3", activity="CRP", timestamp="2014-02-14T08:00:00.000+01:00"))
        # self.assign(self.build_event("case3", activity="Release A", timestamp="2014-07-10T11:52:00.000+02:00"))
        # self.assign(self.build_event("case3", activity="ER Triage", timestamp="2014-07-10T12:06:24.000+02:00"))
        # self.assign(self.build_event("case3", activity="ER Sepsis Triage", timestamp="2014-07-10T12:16:54.000+02:00"))
        # self.assign(self.build_event("case3", activity="CRP", timestamp="2014-07-10T12:50:00.000+02:00"))
        # self.assign(self.build_event("case3", activity="LacticAcid", timestamp="2014-07-10T12:50:00.000+02:00"))
        # self.assign(self.build_event("case3", activity="Leucocytes", timestamp="2014-07-10T12:50:00.000+02:00"))
        # self.assign(self.build_event("case3", activity="IV Liquid", timestamp="2014-07-10T12:56:57.000+02:00"))
        # self.assign(self.build_event("case3", activity="IV Antibiotics", timestamp="2014-07-10T12:57:05.000+02:00"))
        # self.assign(self.build_event("case3", activity="Admission NC", timestamp="2014-07-10T14:07:02.000+02:00"))
        # self.assign(self.build_event("case3", activity="Leucocytes", timestamp="2014-07-12T08:00:00.000+02:00"))
        # self.assign(self.build_event("case3", activity="CRP", timestamp="2014-07-13T08:00:00.000+02:00"))
        # self.assign(self.build_event("case3", activity="Release A", timestamp="2014-07-15T18:00:00.000+02:00"))
        # self.assign(self.build_event("case3", activity="Return ER", timestamp="2014-07-28T17:36:41.000+02:00"))
