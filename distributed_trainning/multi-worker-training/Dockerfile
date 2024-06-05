FROM tensorflow/tensorflow:2.12.0

RUN pip install opencv-python

RUN pip install tqdm

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

COPY . /app

WORKDIR /app

CMD ["python", "mwt.py"]
