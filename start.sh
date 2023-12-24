#!/bin/bash

echo "Docker started."
python forever.py &

cd /app/app/HTTPServer

python main.py 