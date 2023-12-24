FROM starofall/crowdnav

ADD  /app/HTTPServer /app/HTTPServer
COPY  /app/simulation /app/simulation
COPY knobs.json knobs.json
COPY start.sh start.sh
EXPOSE 3000
RUN pip install flask
COPY ./start.sh /app
RUN chmod +x start.sh
CMD ["bash", "start.sh"]