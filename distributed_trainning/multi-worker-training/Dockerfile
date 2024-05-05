FROM tensorflow/tensorflow:2.15.0

RUN pip install tensorflow_datasets==4.9.3

COPY . /app

WORKDIR /app

RUN pip install -r requirement.txt

CMD ["python", "mwt.py"] 
