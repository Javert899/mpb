from iop.algo.discovery import activity_frequency_cases, frequency_performance_dfg, sojourn_time
from iop.algo.conformance import log_skeleton, temporal_profile


class Model(object):
    def __init__(self, log, parameters):
        self.log = log
        self.parameters = parameters
        self.calculate()

    def calculate(self):
        self.activity_frequency_cases = activity_frequency_cases.apply(self.log, parameters=self.parameters)
        self.sojourn_time = sojourn_time.apply(self.log, parameters=self.parameters)
        self.frequency_dfg, self.performance_dfg, self.sa, self.ea, self.af = frequency_performance_dfg.apply(self.log,
                                                                                                              parameters=self.parameters)
        self.lsk, self.lsk_conf = log_skeleton.apply(self.log, parameters=self.parameters)
        self.ts, self.ts_conf = temporal_profile.apply(self.log, parameters=self.parameters)
        print("siii")
