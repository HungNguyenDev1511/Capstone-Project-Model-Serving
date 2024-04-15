FROM tensorflow/tensorflow:2.14.0

RUN pip install tensorflow_datasets==4.9.3

COPY . /app

WORKDIR /app

CMD ["python", "mwt.py"] 

