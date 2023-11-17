FROM starofall/crowdnav

ADD  /app/HTTPServer /app/HTTPServer
COPY knobs.json knobs.json

COPY /app/simulation /app/simulation

WORKDIR /../app
RUN python run.py

WORKDIR /app/HTTPServer
RUN pip install flask

CMD [ "python" , "/app/HTTPServer/main.py" ] 




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
