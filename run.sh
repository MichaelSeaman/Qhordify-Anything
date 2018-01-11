#!/bin/bash

gunicorn server:app -b localhost:8000 "$@"
