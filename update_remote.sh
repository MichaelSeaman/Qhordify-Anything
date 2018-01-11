#!/bin/bash
# To be run on local machine
# Does the following:
# SSH to remote
# updates server repo
# restarts gunicorn as daemon process

HOST="server@ec2-52-27-161-26.us-west-2.compute.amazonaws.com"
REMOTE_REPO_DIR="~/Qhordify-Anything"
SCRIPT="echo \"Successfully connected to ${HOST}\";
echo \"Updating...\"
./update_qhordify_anything.sh;
cd ${REMOTE_REPO_DIR};
echo \"Restarting...\"
./stop.sh;
./run.sh -D;"

ssh -t $HOST "${SCRIPT}"
