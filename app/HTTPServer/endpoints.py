from flask import Flask, jsonify, request
import json 

# Construct the path to the knobs.json file, assuming it's two directories back
json_file_path = '../../knobs.json'

# Open the JSON file in read mode ('r')
with open(json_file_path, 'r') as json_file:
    # Use json.load() to read data from the file
    adaptation_options_data = json.load(json_file)

    # Now 'data' contains the contents of the JSON file as a Python dictionary
    print(adaptation_options_data)

def getAdaptationOptions():
    return adaptation_options_data


