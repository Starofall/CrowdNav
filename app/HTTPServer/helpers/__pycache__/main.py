from flask import jsonify

def getMonitor():
    # Specify the file path
    file_path = "./monitor_data.json"

    try:
        # Open the file in read mode ('r')
        with open(file_path, 'r') as json_file:
            # Use json.load() to read data from the file
            data = json.load(json_file)

        # Now 'data' contains the contents of the JSON file as a Python dictionary
        return jsonify(data)
    
    except FileNotFoundError:
        # Return a 404 Not Found response if the file is not found
        return jsonify({"error": "Monitor data not found"}), 404

    except Exception as e:
        # Handle other exceptions and return a 500 Internal Server Error response
        return jsonify({"error": str(e)}), 500

