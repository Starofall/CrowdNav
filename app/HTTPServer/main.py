from flask import Flask, jsonify
from flask.views import MethodView
import json
from endpoints import get_monitor

app = Flask(__name__)

knobs_path = '../../knobs.json'


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
        try:
            file_path = "./monitor_data.json"
            with open(file_path, "r") as json_file:
                data = json.load(json_file)
            return jsonify(data)
        except FileNotFoundError:
            return jsonify({'error': 'monitor_data.json not found'}), 404


app.add_url_rule('/monitor', view_func=MonitorAPI.as_view('monitor'))


@app.route('/execute', methods=['PUT'])
def execute_adaptation():
    data = get_execute()
    return jsonify(data)


class MonitorSchemaAPI(MethodView):
    def get(self):
        schema = {
            'vehicle_count': 'number',
            'avg_trip_duration': 'number',
            'total_trips': 'number',
            'avg_trip_overhead': 'number',
            'edgeIDs': 'list'
        }
        return jsonify(schema)


app.add_url_rule('/monitor_schema', view_func=MonitorSchemaAPI.as_view('monitor_schema'))


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
                },
                'freshnessCutOffValue': {
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


app.add_url_rule('/adaptation_options_schema', view_func=AdaptationOptionsSchemaAPI.as_view('adaptation_options_schema'))


if __name__ == '__main__':
    app.run(host='0.0.0.0')
