from pm4py.algo.transformation.log_to_features import algorithm as log_to_features
from sklearn import tree
from pm4py.visualization.decisiontree import visualizer as decision_tree_visualizer
from enum import Enum
from pm4py.util import exec_utils, constants, xes_constants


class Parameters(Enum):
    TIMESTAMP_KEY = constants.PARAMETER_CONSTANT_TIMESTAMP_KEY
    START_TIMESTAMP_KEY = constants.PARAMETER_CONSTANT_START_TIMESTAMP_KEY


def apply(log, parameters=None):
    if parameters is None:
        parameters = {}

    start_timestamp_key = exec_utils.get_param_value(Parameters.START_TIMESTAMP_KEY, parameters, xes_constants.DEFAULT_START_TIMESTAMP_KEY)
    timestamp_key = exec_utils.get_param_value(Parameters.TIMESTAMP_KEY, parameters, xes_constants.DEFAULT_TIMESTAMP_KEY)

    try:
        feature, names = log_to_features.apply(log)
        case_durations = []
        for trace in log:
            case_durations.append(trace[-1][timestamp_key].timestamp() - trace[0][start_timestamp_key].timestamp())
        sorted_case_durations = sorted(case_durations)
        fq = sorted_case_durations[int(0.75 * len(sorted_case_durations))]
        classes = ["Under", "Above"]
        target = [0 if case_durations[i] <= fq else 1 for i in range(len(case_durations))]
        clf = tree.DecisionTreeClassifier()
        clf = clf.fit(feature, target)
        gviz = decision_tree_visualizer.apply(clf, names, classes, parameters={"format": "svg"})
        return decision_tree_visualizer.serialize(gviz)
    except:
        return "".encode("utf-8")
