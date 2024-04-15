FROM python:3.8-slim

# Install dependencies
RUN pip3 install kafka-python==2.0.2
RUN pip3 install pandas==1.5.1
RUN pip3 install pymongo==4.5.0

WORKDIR /app

# Copy app handler code
COPY kafka_producer/ /app/

CMD [ "python", "-u", "produce.py", "--mode", "setup", "--bootstrap_servers", "broker:29092"]
