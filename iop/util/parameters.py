from pm4py.util import constants, xes_constants

parameters = {
    constants.PARAMETER_CONSTANT_ACTIVITY_KEY: xes_constants.DEFAULT_NAME_KEY,
    constants.PARAMETER_CONSTANT_TIMESTAMP_KEY: xes_constants.DEFAULT_TIMESTAMP_KEY,
    constants.PARAMETER_CONSTANT_RESOURCE_KEY: xes_constants.DEFAULT_RESOURCE_KEY,
    constants.PARAMETER_CONSTANT_GROUP_KEY: xes_constants.DEFAULT_GROUP_KEY,
    constants.PARAMETER_CONSTANT_CASEID_KEY: xes_constants.DEFAULT_TRACEID_KEY,
    "activity_percentage": 0.2,
    "paths_percentage": 0.2,
    "noise_threshold": 0.02,
    "zeta": 2,
    "business_hours": False
}
