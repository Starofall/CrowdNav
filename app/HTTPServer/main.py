from flask import Flask , jsonify
from app.simulation.Simulation import Simulation
from endpoints import get_monitor , getAdaptationOptions , getexecute

app = Flask(__name__)

@app.route('/monitor', methods=['GET'])
def monitor():
  Simulation.start()

while True:
            # Retrieve real-time data from the simulation
            real_time_data = Simulation.get_real_time_data()
            print("Real-time data from simulation:", real_time_data)
            
            time.sleep(5)  # Adjust the sleep duration based on your requirements

    
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


