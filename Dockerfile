FROM starofall/crowdnav

ADD  /app/HTTPServer /app/HTTPServer
COPY knobs.json knobs.json

# WORKDIR /app

ADD app/simulation/Simulation.py app/simulation/Simulation.py
ADD app/simulation/monitor_data.json app/simulation/monitor_data.json
ADD app/simulation/views.py app/simulation/views.py

# ADD /Config.py /Config.py


# WORKDIR /app/HTTPServer
RUN pip install flask
# WORKDIR /app/HTTPServer
# COPY read_data.py /app/read_data.py

# CMD ["python", "/app/read_data.py"]

CMD [ "python" , "forever.py" ] 
# CMD [ "python" , "/app/HTTPServer/main.py" ] 
# RUN python main.py