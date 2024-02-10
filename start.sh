#!/bin/bash

echo "Docker started."
python forever.py &
python /app/app/HTTPServer/main.py 