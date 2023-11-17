FROM starofall/crowdnav

ADD  /app/HTTPServer /app/HTTPServer
COPY knobs.json knobs.json

# WORKDIR /app

ADD app/simulation/Simulation.py app/simulation/Simulation.py
ADD app/simulation/monitor_data.json app/simulation/monitor_data.json

# ADD /Config.py /Config.py


WORKDIR /app/HTTPServer
RUN pip install flask
# WORKDIR /app/HTTPServer
# COPY read_data.py /app/read_data.py

# CMD ["python", "/app/read_data.py"]

# CMD [ "python" , "forever.py" ] 
CMD [ "python" , "/app/HTTPServer/main.py" ] 
# RUN python main.py





# RUN apt-get update &&              \
#  apt-get install -y             \
 #   build-essential              \
  #  git                          \
   # libxerces-c-dev

#RUN mkdir -p /opt
#RUN (cd /opt; git clone https://github.com/radiganm/sumo.git)
#RUN (cd /opt/sumo; ./configure)
#RUN (cd /opt/sumo; make)
#RUN (cd /opt/sumo; make install)

#ENV SUMO_HOME /opt/sumo
# First cache dependencies
#ADD ./setup.py /app/setup.py
#RUN python /app/setup.py install
# Add sources
#ADD ./ /app/
#WORKDIR /app
#CMD ["python","/app/forever.py"]
