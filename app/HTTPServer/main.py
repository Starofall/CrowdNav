from flask import Flask , jsonify
from endpoints import  getAdaptationOptions , getexecute
import json
import os
import sys


app = Flask(__name__)

@app.route('/monitor', methods=['GET'])
def monitor():
    
    # Retrieve monitored data from the simulation
    # monitored_data = Simulation.get_monitored_data()
    # monitored_data= read_monitored_data()
    file_path = "../simulation/monitor_data.json"
    
    with open(file_path, "r") as json_file:
    # Load the JSON data
            data = json.load(json_file)
    # Return the monitored data as JSON
    print(data)
    return jsonify(data)
    
@app.route('/execute', methods=['PUT'])
def execute_adaptation():
    data = getexecute()
    return jsonify(data)


@app.route('/adaptation_options', methods=['GET'])
def get_adaptation_options():
    data= getAdaptationOptions()
    return jsonify(data)

# @app.route('/monitor_schema', methods=['GET'])
# def get_monitor_schema():
#     field_types = {key: type(value).__name__ for key, value in get_monitor().items()}
#     return field_types

@app.route('/execute_schema', methods=['GET'])
def get_execute_schema():
    return jsonify({"execute_schema": "This is /execute_schema endpoint"})

@app.route('/adaptation_options_schema', methods=['GET'])
def get_adaptation_options_schema():
    return jsonify({"adaptation_options_schema": "This is /adaptation_options_schema endpoint"})

if __name__ == '__main__':
    app.run(debug=True)

