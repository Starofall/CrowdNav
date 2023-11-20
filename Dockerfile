FROM starofall/crowdnav

ADD  /app/HTTPServer /app/HTTPServer
COPY knobs.json knobs.json

WORKDIR /app

COPY . /app 




RUN pip install flask

# ADD /Config.py /Config.py





#WORKDIR /app/
#RUN python forever.py

#WORKDIR /app/
#RUN python forever.py

WORKDIR /app/HTTPServer
CMD [ "python" , "main.py"  ] 

# COPY read_data.py /app/read_data.py

# CMD ["python", "/app/read_data.py"]


# CMD [ "python" , "/app/HTTPServer/main.py" ] 
# RUN python main.py