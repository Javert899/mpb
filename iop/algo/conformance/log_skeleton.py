from collections import Counter

from pm4py.algo.conformance.log_skeleton import algorithm as log_skeleton_conformance
from pm4py.algo.discovery.log_skeleton import algorithm as log_skeleton_discovery
import json
from pm4py.util import xes_constants


def apply(log, parameters=None):
    if parameters is None:
        parameters = {}

    log_skeleton = log_skeleton_discovery.apply(log, parameters=parameters)
    deviations = [x["deviations"] for x in log_skeleton_conformance.apply(log, log_skeleton, parameters=parameters)]
    new_deviations = []

    for index, trace in enumerate(deviations):
        new_deviations.append([])
        for i in range(len(trace)):
            dev = trace[i]
            if dev[0] == "always_before" or dev[0] == "always_after" or dev[
                0] == "never_together" or dev[0] == "equivalence":
                for subdev in dev[1]:
                    new_deviations[-1].append((dev[0], subdev, log[index].attributes[xes_constants.DEFAULT_TRACEID_KEY]))
            elif dev[0] == "activ_freq":
                new_deviations[-1].append(
                    (dev[0], (dev[1][0], list(dev[1][1]) if type(dev[1][1]) is set else [dev[1][1]]), log[index].attributes[xes_constants.DEFAULT_TRACEID_KEY]))
            elif dev[0] == "directly_follows":
                for subdev in dev[1]:
                    new_deviations[-1].append((dev[0], subdev, log[index].attributes[xes_constants.DEFAULT_TRACEID_KEY]))

    json.dumps(new_deviations)

    return new_deviations


def annotation_deviations(lsk, parameters=None):
    if parameters is None:
        parameters = {}

    deviations = Counter()
    lsk = [x for x in lsk if x]
    for trace in lsk:
        this_acts = set()
        for dev in trace:
            if dev[0] == "always_before" or dev[0] == "always_after":
                this_acts.add(dev[1][0])
            elif dev[0] == "never_together":
                this_acts.add(dev[1][0])
                this_acts.add(dev[1][1])
            elif dev[0] == "directly_follows":
                this_acts.add(dev[1][0])
            elif dev[0] == "activ_freq":
                this_acts.add(dev[1][0])
        for act in this_acts:
            deviations[act] += 1
    return dict(deviations)
