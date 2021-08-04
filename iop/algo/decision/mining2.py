from pm4py.algo.transformation.log_to_features import algorithm as log_to_features
from sklearn import tree
from pm4py.visualization.decisiontree import visualizer as decision_tree_visualizer
from enum import Enum
from pm4py.util import exec_utils, constants, xes_constants
from pm4py.statistics.attributes.log import select
import numpy as np

class Parameters(Enum):
    ACTIVITY_KEY = constants.PARAMETER_CONSTANT_ACTIVITY_KEY


def apply(log, dev_cases, parameters=None):
    if parameters is None:
        parameters = {}

    dev_cases = set(dev_cases)

    activity_key = exec_utils.get_param_value(Parameters.ACTIVITY_KEY, parameters, xes_constants.DEFAULT_NAME_KEY)

    classes = ["Normal", "Deviating"]
    target = []

    for i in range(len(log)):
        if i in dev_cases:
            target.append(1)
        else:
            target.append(0)

    try:
        str_tr_attr, str_ev_attr, num_tr_attr, num_ev_attr = select.select_attributes_from_log_for_tree(log)
        str_evsucc_attr = [activity_key]
        str_ev_attr = set(str_ev_attr)
        str_ev_attr.add(activity_key)
        str_ev_attr = list(str_ev_attr)
        new_params = {"str_evsucc_attr": str_evsucc_attr, "str_ev_attr": str_ev_attr, "str_tr_attr": str_tr_attr, "num_tr_attr": num_tr_attr, "num_ev_attr": num_ev_attr}

        feature, names = log_to_features.apply(log, parameters=new_params)
        for i in range(len(feature)):
            for j in range(len(feature[i])):
                try:
                    if np.isnan(feature[i][j]):
                        feature[i][j] = 0
                except:
                    feature[i][j] = 0
        clf = tree.DecisionTreeClassifier(max_depth=5)
        clf = clf.fit(feature, target)
        gviz = decision_tree_visualizer.apply(clf, names, classes, parameters={"format": "svg"})
        return decision_tree_visualizer.serialize(gviz)
    except:
        traceback.print_exc()
        return "".encode("utf-8")
