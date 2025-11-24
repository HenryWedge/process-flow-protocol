import pm4py

from algorithm.sinks.process_flow_sink import ProcessFlowSink
from algorithm.sink_assigner import SinkAssigner
from distributed_environment_builder.infrastructure.network import Network
from distributed_event_factory.configurator import DefConfigurator
from distributed_event_factory.event_factory import EventFactory
from distributed_event_factory.simulation.xes_process_simulator import XesProcessSimulator
from eval_event_log import EvalEventLog
from event_log import EventLog

if __name__ == '__main__':
    configurator = DefConfigurator()
    event_factory = EventFactory()

    network: Network = Network("base")
    sink_assigner = SinkAssigner(
        sink_creator=lambda datasource_refs, node_id: ProcessFlowSink(datasource_refs, node_id, network)
    )

    traffic_fine = EvalEventLog(
        "../../EventFactoryConfigs/Road_Traffic_Fine_Management_Process.xes",
        all_activities=[
            "Create Fine", "Send Fine", "Insert Fine Notification", "Send for Credit Collection", "Payment",
            "Add penalty", "Notify Result Appeal to Offender", "Send Appeal to Prefecture",
            "Insert Date Appeal to Prefecture", "Receive Result Appeal from Prefecture",
            "Notify Result Appeal from Prefecture"
        ]
    )

    sepsis = EvalEventLog(
        "../../EventFactoryConfigs/Sepsis.xes",
        all_activities=[
            ["CRP", "Release B", "Release A", "Release D", "Release C", "Release E", "Admission IC", "Return ER",
             "ER Triage", "IV Antibiotics", "Leucocytes", "ER Registration", "IV Liquid", "Admission NC",
             "LacticAcid", "ER Sepsis Triage"
             ]]
    )

    sepsisDistributed = EvalEventLog(
        "../../EventFactoryConfigs/Sepsis.xes",
        all_activities=[
            ["CRP", "Release B", "Release A", "Release D", "Release C", "Release E"],
            ["Admission IC", "Return ER", "ER Triage", "IV Antibiotics", "Leucocytes", "ER Registration"],
            ["IV Liquid", "Admission NC", "LacticAcid", "ER Sepsis Triage"]
        ]
    )

    log = sepsisDistributed

    # sinks = sink_assigner.assign([
    #    ["Create Fine", "Send Fine"],
    #    ["Insert Fine Notification", "Send for Credit Collection"],
    #    ["Payment", "Add penalty"],
    #    ["Notify Result Appeal to Offender", "Send Appeal to Prefecture"],
    #    ["Insert Date Appeal to Prefecture", "Receive Result Appeal from Prefecture", "Notify Result Appeal from Prefecture"]
    # ])

    sinks = sink_assigner.assign(log.all_activities)
    event_factory = (
        event_factory
        .add_file(configurator.get_simulation_file())
        .add_process_simulator(
            XesProcessSimulator(
                log.path,
                node_key="concept:name",
                group_id_key="concept:name"
            )
        )
    )
    for sink in sinks:
        event_factory = event_factory.add_sink(sink.node_id, sink)
    event_factory.run()

    for sink in sinks:
        petri_net, im, fm = sink.get_model()
        variants = EventLog(sink.get_event_log()).get_variants()
        for trace in variants:
            print(sink.get_heap_size())
            print(f"{trace}:{variants[trace]}")
        print("----")
        view = pm4py.visualization.petri_net.visualizer.apply(petri_net, im, fm)
        pm4py.visualization.petri_net.visualizer.view(view)

    print(network.send_count)
