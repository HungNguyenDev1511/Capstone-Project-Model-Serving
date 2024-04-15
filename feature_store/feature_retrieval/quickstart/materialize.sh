#!/bin/bash
cd ../../feature_repos/quickstart
CURRENT_TIME=$(date -u +"%Y-%m-%dT%H:%M:%S")
feast materialize-incremental $CURRENT_TIME