from pm4py.algo.discovery.log_skeleton import algorithm as log_skeleton_discovery
from pm4py.algo.conformance.log_skeleton import algorithm as log_skeleton_conformance


def apply(log, parameters=None):
    if parameters is None:
        parameters = {}

    log_skeleton = log_skeleton_discovery.apply(log, parameters=parameters)
    return log_skeleton_conformance.apply(log, log_skeleton, parameters=parameters)
