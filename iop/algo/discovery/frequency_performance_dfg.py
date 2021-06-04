from enum import Enum

from pm4py.algo.discovery.dfg import algorithm as dfg_discovery
from pm4py.algo.filtering.dfg import dfg_filtering
from pm4py.statistics.attributes.log import get as attributes_get
from pm4py.statistics.end_activities.log import get as ea_get
from pm4py.statistics.start_activities.log import get as sa_get
from pm4py.util import xes_constants, exec_utils


class Parameters(Enum):
    ACTIVITY_PERCENTAGE = "activity_percentage"
    PATHS_PERCENTAGE = "paths_percentage"


def apply(log, parameters=None):
    if parameters is None:
        parameters = {}

    frequency_dfg = dfg_discovery.apply(log, parameters=parameters)
    performance_dfg = dfg_discovery.apply(log, parameters=parameters)

    af = attributes_get.get_attribute_values(log, xes_constants.DEFAULT_NAME_KEY, parameters=parameters)
    sa = sa_get.get_start_activities(log, parameters=parameters)
    ea = ea_get.get_end_activities(log, parameters=parameters)

    activity_percentage = exec_utils.get_param_value(Parameters.ACTIVITY_PERCENTAGE, parameters, 1.0)
    paths_percentage = exec_utils.get_param_value(Parameters.PATHS_PERCENTAGE, parameters, 1.0)

    frequency_dfg, sa, ea, af = dfg_filtering.filter_dfg_on_activities_percentage(frequency_dfg, sa, ea, af,
                                                                                  activity_percentage)
    frequency_dfg, sa, ea, af = dfg_filtering.filter_dfg_on_paths_percentage(frequency_dfg, sa, ea, af,
                                                                             paths_percentage)

    performance_dfg = {x: y for x, y in performance_dfg.items() if x in frequency_dfg}

    return frequency_dfg, performance_dfg, sa, ea, af
