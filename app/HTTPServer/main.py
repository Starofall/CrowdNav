from flask import Flask , jsonify
from endpoints import get_monitor , getAdaptationOptions , getexecute

import os
import sys

# Get the path to the parent directory of the package
package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Add the parent directory to the Python path
sys.path.append(package_path)

# Now you can import your module
from simulation.Simulation import Simulation

app = Flask(__name__)

@app.route('/monitor', methods=['GET'])
def monitor():
    # Retrieve monitored data from the simulation
    monitored_data = Simulation.get_monitored_data()

    # Return the monitored data as JSON
    return jsonify(monitored_data)
    
@app.route('/execute', methods=['PUT'])
def execute_adaptation():
    data = getexecute()
    return jsonify(data)


@app.route('/adaptation_options', methods=['GET'])
def get_adaptation_options():
    data= getAdaptationOptions()
    return jsonify(data)

@app.route('/monitor_schema', methods=['GET'])
def get_monitor_schema():
    field_types = {key: type(value).__name__ for key, value in get_monitor().items()}
    return field_types

@app.route('/execute_schema', methods=['GET'])
def get_execute_schema():
    return jsonify({"execute_schema": "This is /execute_schema endpoint"})

@app.route('/adaptation_options_schema', methods=['GET'])
def get_adaptation_options_schema():
    return jsonify({"adaptation_options_schema": "This is /adaptation_options_schema endpoint"})

if __name__ == '__main__':
    app.run(debug=True)

