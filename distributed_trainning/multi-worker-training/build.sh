#!/bin/bash
IMAGE=6666688889/distributed_training:0.0.11
docker build -t $IMAGE .
docker push $IMAGE