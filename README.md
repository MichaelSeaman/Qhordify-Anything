# Qhordify Anything
A python/flask/gunicorn webserver for running 'Qhordify Anything' - a web backend for serving the [quantum-performance](https://github.com/MichaelSeaman/quantum_performance) package.

## Dependencies:
Qhordify-Anything requires:

* nginx
* python3
* flask
* gunicorn

## Running the server:
The server can be started from a terminal with:
```
gunicorn server:app -b localhost:8000
```
or, more simply by running the script ```run.sh```. Passing the option ```-D``` to either of these commands allows them to be run as background daemon processes.
