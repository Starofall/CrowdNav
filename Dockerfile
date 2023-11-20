FROM starofall/crowdnav

ADD  /app/HTTPServer /app/HTTPServer
COPY knobs.json knobs.json

WORKDIR /app

COPY . /app 
RUN pip install flask

WORKDIR /app/HTTPServer
CMD [ "python" , "main.py"  ] 
