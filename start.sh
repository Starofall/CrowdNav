#!/bin/bash

# cd /app/HTTPServer 
echo "Docker started."
python forever.py &

cd /app/app/HTTPServer

python main.py 