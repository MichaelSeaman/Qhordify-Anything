#!/bin/bash

gunicorn server:app -t 300 --error-logfile error.log --access-logfile access.log -b localhost:8000 "$@"
