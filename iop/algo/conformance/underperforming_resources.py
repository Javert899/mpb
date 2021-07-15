import json
from pm4py.util import constants, exec_utils, xes_constants
from enum import Enum
from copy import copy
from statistics import mean, stdev


class Parameters(Enum):
    ACTIVITY_KEY = constants.PARAMETER_CONSTANT_ACTIVITY_KEY
    START_TIMESTAMP_KEY = constants.PARAMETER_CONSTANT_START_TIMESTAMP_KEY
    TIMESTAMP_KEY = constants.PARAMETER_CONSTANT_TIMESTAMP_KEY
    RESOURCE_KEY = constants.PARAMETER_CONSTANT_RESOURCE_KEY
    CASE_ID_KEY = constants.PARAMETER_CONSTANT_CASEID_KEY
    ZETA = "zeta"


def apply(log, parameters=None):
    if parameters is None:
        parameters = {}

    activity_key = exec_utils.get_param_value(Parameters.ACTIVITY_KEY, parameters, xes_constants.DEFAULT_NAME_KEY)
    start_timestamp_key = exec_utils.get_param_value(Parameters.START_TIMESTAMP_KEY, parameters, xes_constants.DEFAULT_START_TIMESTAMP_KEY)
    timestamp_key = exec_utils.get_param_value(Parameters.TIMESTAMP_KEY, parameters, xes_constants.DEFAULT_TIMESTAMP_KEY)
    case_id_key = exec_utils.get_param_value(Parameters.CASE_ID_KEY, parameters, xes_constants.DEFAULT_TRACEID_KEY)
    resource_key = exec_utils.get_param_value(Parameters.RESOURCE_KEY, parameters, xes_constants.DEFAULT_RESOURCE_KEY)
    zeta = exec_utils.get_param_value(Parameters.ZETA, parameters, 1)

    perf_act = {}
    for trace in log:
        for event in trace:
            act = event[activity_key]
            st = event[start_timestamp_key].timestamp()
            et = event[timestamp_key].timestamp()
            perf = et - st
            if act not in perf_act:
                perf_act[act] = [perf]
            else:
                perf_act[act].append(perf)

    act_keys = list(perf_act)
    for act in act_keys:
        if len(perf_act[act]) == 1:
            del perf_act[act]
        perf_act[act] = (mean(perf_act[act]), stdev(perf_act[act]))
        if perf_act[act][1] < 0.00001:
            del perf_act[act]

    perf_act_res = {}
    try:
        for trace in log:
            for event in trace:
                act = event[activity_key]
                if act in perf_act:
                    res = event[resource_key]
                    if str(res).lower() != "none" and str(res).lower() != "nan":
                        st = event[start_timestamp_key].timestamp()
                        et = event[timestamp_key].timestamp()
                        perf = et - st
                        if perf > (perf_act[act][0] + zeta * perf_act[act][1]):
                            if act not in perf_act_res:
                                perf_act_res[act] = []
                            perf_act_res[act].append((res, act, trace.attributes[case_id_key], perf, (perf - perf_act[act][0]) / perf_act[act][1]))
    except:
        pass

    return perf_act_res


def annotation_deviations(perf_act_res, parameters=None):
    if parameters is None:
        parameters = {}

    return perf_act_res


def all_resource_deviations(perf_act_res, parameters=None):
    if parameters is None:
        parameters = {}

    ret = {}
    for act in perf_act_res:
        for el in perf_act_res[act]:
            res = el[0]
            if res not in ret:
                ret[res] = []
            ret[res].append(el)

    return ret
