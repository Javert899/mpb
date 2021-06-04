from pm4py.algo.discovery.temporal_profile import algorithm as temporal_profile_discovery
from pm4py.algo.conformance.temporal_profile import algorithm as temporal_profile_conformance
from collections import Counter
import json


def apply(log, parameters=None):
    if parameters is None:
        parameters = {}

    ts = temporal_profile_discovery.apply(log, parameters=parameters)
    conf = temporal_profile_conformance.apply(log, ts, parameters=parameters)

    json.dumps(conf)

    return conf


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
