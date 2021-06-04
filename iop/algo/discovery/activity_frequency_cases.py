from pm4py.util import xes_constants
from pm4py.statistics.attributes.log import get as attributes_get
from copy import copy
import json


def apply(log, parameters=None):
    if parameters is None:
        parameters = {}

    this_parameters = copy(parameters)
    this_parameters["keep_once_per_case"] = True

    ret = attributes_get.get_attribute_values(log, xes_constants.DEFAULT_NAME_KEY, parameters=this_parameters)

    json.dumps(ret)

    return ret
