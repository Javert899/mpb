from iop.algo.discovery import activity_frequency_cases, frequency_performance_dfg, sojourn_time, case_ids
from iop.algo.conformance import log_skeleton, temporal_profile, underperforming_resources
import json
import frozendict
from iop.algo.decision import mining

models_dictio = {}


class Model(object):
    def __init__(self, log, parameters):
        self.log = log
        self.parameters = parameters
        self.calculate()

    def calculate(self):
        print("1")
        self.case_ids = case_ids.apply(self.log, parameters=self.parameters)
        print("2")
        self.activity_frequency_cases = activity_frequency_cases.apply(self.log, parameters=self.parameters)
        print("3")
        self.sojourn_time = sojourn_time.apply(self.log, parameters=self.parameters)
        print("4")
        self.frequency_dfg, self.performance_dfg, self.sa, self.ea, self.af = frequency_performance_dfg.apply(self.log,
                                                                                                              parameters=self.parameters)
        print("5")
        self.lsk, self.lsk_conf = log_skeleton.apply(self.log, parameters=self.parameters)
        print("6")
        self.ts, self.ts_conf = temporal_profile.apply(self.log, parameters=self.parameters)
        print("7")
        self.ur = underperforming_resources.apply(self.log, parameters=self.parameters)
        print("8")
        self.decision_tree = mining.apply(self.log, parameters=self.parameters)
        print("9")


    def get_lsk_conf_cases(self):
        return self.lsk_conf

    def get_ts_conf_cases(self):
        return self.ts_conf

    def get_activity_lsk_conf(self):
        dev = log_skeleton.all_activity_deviations(self.log, self.lsk_conf, parameters=self.parameters)
        return dev

    def get_activity_ts_conf(self):
        dev = temporal_profile.all_activity_deviations(self.log, self.ts_conf, parameters=self.parameters)
        return dev

    def get_cases_ur(self):
        return underperforming_resources.case_deviations(self.ur, parameters=self.parameters)

    def get_resource_ur(self):
        return underperforming_resources.all_resource_deviations(self.ur, parameters=self.parameters)

    def get_case_ids(self):
        return self.case_ids

    def get_decision_tree(self):
        return self.decision_tree

    def get_model(self):
        ret = {"activity_frequency_cases": self.activity_frequency_cases,
               "sojourn_time": self.sojourn_time, "frequency_dfg": self.frequency_dfg, "performance_dfg": self.performance_dfg,
               "start_activities": self.sa, "end_activities": self.ea, "activities_frequency": self.af,
               "lsk_annotations": log_skeleton.annotation_deviations(self.lsk_conf, parameters=self.parameters),
               "ts_annotations": temporal_profile.annotation_deviations(self.ts_conf, parameters=self.parameters),
               "ur_annotations": underperforming_resources.annotation_deviations(self.ur, parameters=self.parameters)}
        return ret


def apply(log, parameters):
    parameters_frozen = frozendict.frozendict(parameters)
    tup = (id(log), parameters_frozen)
    if tup in models_dictio:
        return models_dictio[tup]
    else:
        model = Model(log, parameters)
        models_dictio[tup] = model
        return model
