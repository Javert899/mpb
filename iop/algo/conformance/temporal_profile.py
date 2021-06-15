from pm4py.algo.discovery.temporal_profile import algorithm as temporal_profile_discovery
from pm4py.algo.conformance.temporal_profile import algorithm as temporal_profile_conformance
from collections import Counter
from pm4py.util import xes_constants
import json


def apply(log, parameters=None):
    if parameters is None:
        parameters = {}

    ts = temporal_profile_discovery.apply(log, parameters=parameters)
    conf = temporal_profile_conformance.apply(log, ts, parameters=parameters)

    for i1, trace in enumerate(conf):
        for i2, dev in enumerate(trace):
            trace[i2] = tuple(list(trace[i2]) + [log[i1].attributes[xes_constants.DEFAULT_TRACEID_KEY]])

    json.dumps(conf)

    return ts, conf


def annotation_deviations(tsc, parameters=None):
    if parameters is None:
        parameters = {}

    deviations = Counter()

    for trace in tsc:
        dev_act = set(x[1] for x in trace)
        for act in dev_act:
            deviations[act] += 1

    ret = dict(deviations)

    json.dumps(ret)

    return ret


def all_activity_deviations(log, tsc, parameters=None):
    if parameters is None:
        parameters = {}

    activity_deviations = {}
    tsc = [x for x in tsc if x]

    for trace in tsc:
        for dev in trace:
            act = dev[1]
            if act not in activity_deviations:
                activity_deviations[act] = []
            activity_deviations[act].append(dev)

    json.dumps(activity_deviations)

    return activity_deviations
