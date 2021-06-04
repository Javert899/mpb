from pm4py.statistics.sojourn_time.log import get as sojourn_time_get
import json


def apply(log, parameters=None):
    if parameters is None:
        parameters = {}

    ret = sojourn_time_get.apply(log, parameters=parameters)

    json.dumps(ret)

    return ret
