from flask import Flask, render_template, request, make_response, jsonify, redirect, url_for
import base64, os
from tempfile import NamedTemporaryFile
import uuid
from iop.objects.log import df_loader, log_loader
from copy import copy
from iop.objects.model import model as model_factory
from iop.algo.decision import mining2
from flask_cors import CORS
import json
import traceback


app = Flask(__name__)
CORS(app, expose_headers=["x-suggested-filename"])


logs_dictio = {}


@app.route('/')
def empty_path():
    return redirect(url_for('upload_page'))


@app.route('/index.html')
def index():
    return redirect(url_for('upload_page'))


@app.route('/upload.html')
def upload_page():
    response = make_response(render_template('upload.html'))
    return response


@app.route('/process.html')
def process_page():
    response = make_response(render_template('process.html'))
    return response


@app.route("/uploadService", methods=["POST"])
def upload():
    this_uuid = ""
    for file in request.files:
        tmp_file = NamedTemporaryFile()
        tmp_file.close()
        fo = request.files[file]
        fo.save(tmp_file.name)
        this_uuid = __load_log(file, tmp_file.name)
    return {"uuid": this_uuid}


@app.route("/processService")
def process():
    uuid = request.args.get("uuid")
    parameters_url = request.args.get("parameters")
    try:
        parameters = base64.b64decode(parameters_url)
        extra_parameters = json.loads(parameters)
    except:
        traceback.print_exc()
        extra_parameters = {}
    #uuid_example_log = __load_log("inputs/interval_event_log.xes", "inputs/interval_event_log.xes")
    return __get_process(uuid, extra_parameters)


@app.route("/decisionTreeService")
def decisionTreeService():
    uuid = request.args.get("uuid")
    parameters_url = request.args.get("parameters")
    try:
        parameters = base64.b64decode(parameters_url)
        extra_parameters = json.loads(parameters)
    except:
        traceback.print_exc()
        extra_parameters = {}

    log, parameters = logs_dictio[uuid]
    parameters = copy(parameters)
    for param in extra_parameters:
        parameters[param] = extra_parameters[param]
    deviating_cases = parameters["deviating_cases"]

    return mining2.apply(log, deviating_cases, parameters=parameters)


def __load_log(orig_name, path):
    this_uuid = str(uuid.uuid4())
    try:
        log, parameters = log_loader.apply(path)
    except:
        log, parameters = df_loader.apply(path)
    logs_dictio[this_uuid] = (log, parameters)
    return this_uuid


def __get_process(uuid, extra_parameters=None):
    if extra_parameters is None:
        extra_parameters = {}
    log, parameters = logs_dictio[uuid]
    parameters = copy(parameters)
    for param in extra_parameters:
        parameters[param] = extra_parameters[param]
    model = model_factory.apply(log, parameters)
    ret = {}
    ret["model"] = model.get_model()
    ret["uuid"] = uuid
    ret["case_ids"] = model.get_case_ids()
    ret["lsk_conf_cases"] = model.get_lsk_conf_cases()
    ret["ts_conf_cases"] = model.get_ts_conf_cases()
    ret["activity_lsk_conf"] = model.get_activity_lsk_conf()
    ret["activity_ts_conf"] = model.get_activity_ts_conf()
    ret["cases_ur"] = model.get_cases_ur()
    ret["resource_ur"] = model.get_resource_ur()
    ret["decision_tree"] = model.get_decision_tree().decode('utf-8')
    return jsonify(ret)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
