from pm4py.statistics.sojourn_time.log import get as sojourn_time_get


def apply(log, parameters=None):
    if parameters is None:
        parameters = {}

    return sojourn_time_get.apply(log, parameters=parameters)
