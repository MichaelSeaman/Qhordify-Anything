#!/bin/bash

kill -9 `ps aux |grep gunicorn | awk '{ print $2 }'`  # will kill all of the workers
