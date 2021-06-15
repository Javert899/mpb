from iop.algo.discovery import activity_frequency_cases, frequency_performance_dfg, sojourn_time, case_ids
from iop.algo.conformance import log_skeleton, temporal_profile
import json
import frozendict

models_dictio = {}


class Model(object):
    def __init__(self, log, parameters):
        self.log = log
        self.parameters = parameters
        self.calculate()

    def calculate(self):
        self.case_ids = case_ids.apply(self.log, parameters=self.parameters)
        self.activity_frequency_cases = activity_frequency_cases.apply(self.log, parameters=self.parameters)
        self.sojourn_time = sojourn_time.apply(self.log, parameters=self.parameters)
        self.frequency_dfg, self.performance_dfg, self.sa, self.ea, self.af = frequency_performance_dfg.apply(self.log,
                                                                                                              parameters=self.parameters)
        self.lsk, self.lsk_conf = log_skeleton.apply(self.log, parameters=self.parameters)
        self.ts, self.ts_conf = temporal_profile.apply(self.log, parameters=self.parameters)

    def get_lsk_conf_cases(self):
        return json.dumps(self.lsk_conf)

    def get_ts_conf_cases(self):
        return json.dumps(self.ts_conf)

    def get_activity_lsk_conf(self):
        dev = log_skeleton.all_activity_deviations(self.log, self.lsk_conf, parameters=self.parameters)
        return json.dumps(dev)

    def get_activity_ts_conf(self):
        dev = temporal_profile.all_activity_deviations(self.log, self.ts_conf, parameters=self.parameters)
        return json.dumps(dev)


def apply(log, parameters):
    parameters_frozen = frozendict.frozendict(parameters)
    tup = (id(log), parameters_frozen)
    if tup in models_dictio:
        return models_dictio[tup]
    else:
        model = Model(log, parameters)
        models_dictio[tup] = model
        return model
