FROM starofall/crowdnav

COPY . .
RUN pip install flask
COPY ./start.sh /app
EXPOSE 5000
WORKDIR /app
RUN chmod 777 ./start.sh

CMD ["bash", "start.sh"]
