#!/bin/bash

gunicorn server:app -t 300 -b localhost:8000 "$@"
