from pm4py.util import constants, xes_constants, exec_utils
from enum import Enum
import json


class Parameters(Enum):
    CASE_ID_KEY = constants.PARAMETER_CONSTANT_CASEID_KEY


def apply(log, parameters=None):
    if parameters is None:
        parameters = {}

    case_id = exec_utils.get_param_value(Parameters.CASE_ID_KEY, parameters, xes_constants.DEFAULT_TRACEID_KEY)
    ret = []
    for trace in log:
        ret.append(trace.attributes[case_id])
    json.dumps(ret)
    return ret
