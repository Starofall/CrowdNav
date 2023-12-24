#!/bin/bash

echo "Docker started."
python forever.py &
cd /app/HTTPServer 
python main.py 