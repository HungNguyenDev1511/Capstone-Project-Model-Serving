FROM tensorflow/tensorflow:2.14.0

RUN pip install ultralytics
RUN pip install -U ray[tune]
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

COPY . /app

WORKDIR /app

CMD ["python", "mwt.py"] 

