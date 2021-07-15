from iop.util.parameters import parameters as default_parameters
from copy import copy
import pm4py
from pm4py.statistics.attributes.log import get as attributes_get
from pm4py.util import constants, xes_constants
from pm4py.objects.log.util import interval_lifecycle
from pm4py.objects.log.importer.xes import importer as xes_importer


def apply(log_path, max_traces=100000000000000):
    parameters = copy(default_parameters)
    log = xes_importer.apply(log_path, parameters={"show_progress_bar": False, "max_traces": max_traces})
    try:
        transitions = attributes_get.get_attribute_values(log, constants.PARAMETER_CONSTANT_TRANSITION_KEY)
        if len(transitions) > 2:
            # convert the event log to an interval event log
            log = interval_lifecycle.to_interval(log)
    except:
        pass

    # checks if the first event of the log contains the start timestamp
    if xes_constants.DEFAULT_START_TIMESTAMP_KEY in log[0][0]:
        parameters[constants.PARAMETER_CONSTANT_START_TIMESTAMP_KEY] = xes_constants.DEFAULT_START_TIMESTAMP_KEY
    else:
        parameters[constants.PARAMETER_CONSTANT_START_TIMESTAMP_KEY] = xes_constants.DEFAULT_TIMESTAMP_KEY

    return log, parameters
