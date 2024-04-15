#!/bin/bash
IMAGE=fullstackdatascience/distributed_training:0.0.11
docker build -t $IMAGE .
docker push $IMAGE