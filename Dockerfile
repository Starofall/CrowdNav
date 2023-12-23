FROM starofall/crowdnav

COPY . .

# WORKDIR /app

# COPY . /app 
RUN pip install flask

COPY ./start.sh /app

# WORKDIR /app

EXPOSE 5000

WORKDIR /app

RUN chmod 777 ./start.sh

CMD ["bash", "start.sh"]
