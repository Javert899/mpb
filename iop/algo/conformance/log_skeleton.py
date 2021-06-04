from pm4py.algo.discovery.log_skeleton import algorithm as log_skeleton_discovery
from pm4py.algo.conformance.log_skeleton import algorithm as log_skeleton_conformance
from collections import Counter


def apply(log, parameters=None):
    if parameters is None:
        parameters = {}

    log_skeleton = log_skeleton_discovery.apply(log, parameters=parameters)
    return [x["deviations"] for x in log_skeleton_conformance.apply(log, log_skeleton, parameters=parameters)]


def activity_deviations(lsk, parameters=None):
    if parameters is None:
        parameters = {}

    deviations = Counter()
    lsk = [x for x in lsk if x]
    for trace in lsk:
        this_acts = set()
        for dev in trace:
            if dev[0] == "always_before":
                for subdev in dev[1]:
                    this_acts.add(subdev[1])
            elif dev[0] == "directly_follows":
                for subdev in dev[1]:
                    this_acts.add(subdev[1])
            elif dev[0] == "activ_freq":
                this_acts.add(dev[1][0])
            elif dev[0] == "always_after":
                for subdev in dev[1]:
                    this_acts.add(subdev[1])
            elif dev[0] == "never_together":
                for subdev in dev[1]:
                    this_acts.add(subdev[0])
                    this_acts.add(subdev[1])
        for act in this_acts:
            deviations[act] += 1
    return dict(deviations)
