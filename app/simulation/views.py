from flask import jsonify
from flask.views import MethodView
# from endpoints import getAdaptationOptions, getexecute
import json

class MonitorAPI(MethodView):
    def get(self):
        file_path = "./monitor_data.json"
        with open(file_path, "r") as json_file:
            data = json.load(json_file)
        return jsonify(data)

class ExecuteAPI(MethodView):
    def put(self):
        # data = getexecute()
        return jsonify({"execute_schema": "This is /execute_schema endpoint"})

class AdaptationOptionsAPI(MethodView):
    def get(self):
        # data = getAdaptationOptions()
        return jsonify({"AdaptationOptionsAPI": "This is /AdaptationOptionsAPI endpoint"})

class ExecuteSchemaAPI(MethodView):
    def get(self):
        return jsonify({"execute_schema": "This is /execute_schema endpoint"})

class AdaptationOptionsSchemaAPI(MethodView):
    def get(self):
        return jsonify({"adaptation_options_schema": "This is /adaptation_options_schema endpoint"})

