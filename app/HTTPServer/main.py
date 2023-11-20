from flask import Flask, jsonify, request
from flask.views import MethodView
import json
import os
app = Flask(__name__)

knobs_path = '../../knobs.json'
monitor_data_path = os.path.join(os.path.dirname(__file__), '..', 'simulation', 'monitor_data.json')
def read_knobs():
    """Read the knobs.json file."""
    try:
        with open(knobs_path, 'r') as file:
            knobs_data = json.load(file)
        return knobs_data
    except FileNotFoundError:
        return None

def write_knobs(data):
    """Write data to the knobs.json file."""
    with open(knobs_path, 'w') as file:
        json.dump(data, file, indent=2)

class MonitorAPI(MethodView):
    def get(self):
        # try:
        with open(monitor_data_path, "r") as json_file:
            data = json.load(json_file)
        return jsonify(data)
        # except FileNotFoundError:
            # return jsonify({'error': 'monitor_data.json not found'}), 404

class ExecuteAPI(MethodView):
    def put(self):
        try:
            data = request.get_json()
            
            return jsonify({'success': True})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

class AdaptationOptionsAPI(MethodView):
    def get(self):
        knobs_data = read_knobs()
        if knobs_data is not None:
            return jsonify(knobs_data)
        else:
            return jsonify({'error': 'knobs.json not found'}), 404

    def put(self):
        try:
            data = request.get_json()
            write_knobs(data)
            return jsonify({'success': True})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

class MonitorSchemaAPI(MethodView):
    def monitor_schema():
        schema = {
            'type': 'object',
            'properties': {
            'vehicle_count': {'type': 'integer'},
            'avg_trip_duration': {'type': 'number'},
            'total_trips': {'type': 'integer'},
            'avg_trip_overhead': {'type': 'number'}
          },
            'required': ['vehicle_count', 'avg_trip_duration', 'total_trips', 'avg_trip_overhead']
        }
        return jsonify(schema)

class ExecuteSchemaAPI(MethodView):
    def get(self):
        schema = {
            'type': 'object',
            'properties': {
                'routeRandomSigma': {
                    'type': 'number',
                    'description': 'The randomization sigma of edge weights'
                },
                'explorationPercentage': {
                    'type': 'number',
                    'description': 'The percentage of routes used for exploration'
                },
                'maxSpeedAndLengthFactor': {
                    'type': 'integer',
                    'description': 'How much the length/speed influences the routing'
                },
                'averageEdgeDurationFactor': {
                    'type': 'integer',
                    'description': 'How much the average edge factor influences the routing'
                },
                'freshnessUpdateFactor': {
                    'type': 'integer',
                    'description': 'How much the freshness update factor influences the routing'
                },'freshnessCutOffValue': {
                    'type': 'integer',
                    'description': 'If data is older than this, it is not considered in the algorithm'
                },
                'reRouteEveryTicks': {
                    'type': 'integer',
                    'description': 'Check for a new route every x times after the car starts'
                },
                # Add more properties as needed
            },
            'required': [
                'routeRandomSigma',
                'explorationPercentage',
                'maxSpeedAndLengthFactor',
                'averageEdgeDurationFactor',
                'freshnessUpdateFactor',
                'freshnessCutOffValue',
                'reRouteEveryTicks'
            ],
        }
        return jsonify(schema)

class AdaptationOptionsSchemaAPI(MethodView):
    def get(self):
        schema = {
            'type': 'object',
            'properties': {
                'routeRandomSigma': {
                    'type': 'number',
                    'description': 'The randomization sigma of edge weights'
                },
                'explorationPercentage': {
                    'type': 'number',
                    'description': 'The percentage of routes used for exploration'
                },
                'maxSpeedAndLengthFactor': {
                    'type': 'integer',
                    'description': 'How much the length/speed influences the routing'
                },
                'averageEdgeDurationFactor': {
                    'type': 'integer',
                    'description': 'How much the average edge factor influences the routing'
                },
                'freshnessUpdateFactor': {
                    'type': 'integer',
                    'description': 'How much the freshness update factor influences the routing'
                },'freshnessCutOffValue': {
                    'type': 'integer',
                    'description': 'If data is older than this, it is not considered in the algorithm'
                },
                'reRouteEveryTicks': {
                    'type': 'integer',
                    'description': 'Check for a new route every x times after the car starts'
                },
                # Add more properties as needed
            },
            'required': [
                'routeRandomSigma',
                'explorationPercentage',
                'maxSpeedAndLengthFactor',
                'averageEdgeDurationFactor',
                'freshnessUpdateFactor',
                'freshnessCutOffValue',
                'reRouteEveryTicks'
            ],
        }
        return jsonify(schema)


if __name__ == '__main__':
    # Registering the views
    app.add_url_rule('/monitor', view_func=MonitorAPI.as_view('monitor_api'))
    app.add_url_rule('/execute', view_func=ExecuteAPI.as_view('execute_api'))
    app.add_url_rule('/adaptation_options', view_func=AdaptationOptionsAPI.as_view('adaptation_options_api'))
    app.add_url_rule('/execute_schema', view_func=ExecuteSchemaAPI.as_view('execute_schema_api'))
    app.add_url_rule('/adaptation_options_schema', view_func=AdaptationOptionsSchemaAPI.as_view('adaptation_options_schema_api'))
    app.add_url_rule('/monitor_schema', view_func=MonitorSchemaAPI.as_view('monitor_schema_api'))
    app.run(host='0.0.0.0', port=5000)
