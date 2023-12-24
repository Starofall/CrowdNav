from flask import Flask, jsonify
from flask.views import MethodView
import json
from endpoints import  getexecute

app = Flask(__name__)

knobs_path = '../../knobs.json'


@app.route('/monitor', methods=['GET'])
def get():
    try:
        file_path = "./monitor_data.json"
        with open(file_path, "r") as json_file:
            data = json.load(json_file)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({'error': 'monitor_data.json not found'}), 404




@app.route('/execute', methods=['PUT'])
def execute_adaptation():
    data = getexecute()
    return jsonify(data)

@app.route('/monitor_schema', methods=['PUT'])
def get():
        schema = {
            'vehicle_count': 'number',
            'avg_trip_duration': 'number',
            'total_trips': 'number',
            'avg_trip_overhead': 'number',
            'edgeIDs': 'list'
        }
        return jsonify(schema)


@app.route('/adaptation_options_schema', methods=['PUT'])
def get():
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



if __name__ == '__main__':
    app.run(host='0.0.0.0')
