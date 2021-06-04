from pm4py.util import xes_constants
from pm4py.statistics.attributes.log import get as attributes_get


def apply(log, parameters=None):
    if parameters is None:
        parameters = {}

    return attributes_get.get_attribute_values(log, xes_constants.DEFAULT_NAME_KEY, parameters=parameters)
