#!/bin/bash

# Call after setting the environment vars
./gcp_scripts/build_and_push.sh

# Call after image is built and pushed to GCP
./gcp_scripts/deploy_and_schedule.sh
