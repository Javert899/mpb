import pandas as pd
import pm4py
from pm4py.util import constants, xes_constants
from copy import copy
from iop.util.parameters import parameters as default_parameters


def apply(log_path):
    parameters = copy(default_parameters)
    df = pd.read_csv(log_path)
    parameters[constants.PARAMETER_CONSTANT_CASEID_KEY] = constants.CASE_CONCEPT_NAME
    if xes_constants.DEFAULT_START_TIMESTAMP_KEY in df.columns:
        parameters[constants.PARAMETER_CONSTANT_START_TIMESTAMP_KEY] = xes_constants.DEFAULT_START_TIMESTAMP_KEY
    else:
        parameters[constants.PARAMETER_CONSTANT_START_TIMESTAMP_KEY] = xes_constants.DEFAULT_TIMESTAMP_KEY
    return pm4py.convert_to_event_log(df), parameters