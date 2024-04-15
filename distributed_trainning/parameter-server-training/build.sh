#!/bin/bash
IMAGE=fullstackdatascience/parameter_server_training:0.0.43
docker build -t $IMAGE .
docker push $IMAGE