from flask import Flask, request, send_from_directory
from flask import safe_join, redirect, url_for
from flask import after_this_request
from werkzeug.utils import secure_filename
import os
import shutil
import sys
from time import sleep
import datetime
from threading import Thread


sys.path.append('quantum_performance')
from quantum_performance import *

if not os.path.exists('uploads'):
    os.makedirs('uploads')

if not os.path.exists('downloads'):
    os.makedirs('downloads')

if not os.path.exists('temp'):
    os.makedirs('temp')

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
DOWNLOAD_FOLDER = 'downloads'
TEMP_FOLDER = 'temp'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 128 * 1024

print("Running ", sys.version)

@app.route("/", methods=['GET','POST'])
def serve_main():
    if request.method == 'GET':
        return app.send_static_file('index.html')

    elif request.method == 'POST':
        try:
            if 'midi_file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            f = request.files['midi_file']
            filename = secure_filename(f.filename)
            print("Recieved",filename)

            upload_ts_dir, temp_ts_dir, download_ts_dir, stamp, in_filepath, \
                temp_filepath, out_filepath = setup_directories(filename)

            f.save(in_filepath)
            QP(in_filepath, temp_filepath, out_filepath)
            del_thread = Thread(target=delayed_delete, args=(
                30, [upload_ts_dir, temp_ts_dir, download_ts_dir]))
            del_thread.start()
            print(url_for('ready_file', filename=filename, ts_dir=stamp))
            return redirect(url_for('ready_file', filename=filename, ts_dir=stamp))
        except Exception as e:
            print(e)
            return redirect(url_for('serve_error'))


@app.route('/error.html')
def serve_error():
    return app.send_static_file('error.html')

@app.route('/downloads/<ts_dir>/<filename>')
def ready_file(filename, ts_dir):
    out_dir = os.path.join(DOWNLOAD_FOLDER, ts_dir)
    return send_from_directory(out_dir, filename)

def setup_directories(filename):
    upload_ts_dir, _ = create_timestamp_dir(UPLOAD_FOLDER)
    temp_ts_dir, _ = create_timestamp_dir(TEMP_FOLDER)
    download_ts_dir, stamp = create_timestamp_dir(DOWNLOAD_FOLDER)

    in_filepath = safe_join(upload_ts_dir, filename)
    temp_filepath = safe_join(temp_ts_dir, swap_extension(filename, "csv"))
    out_filepath = safe_join(download_ts_dir, filename)
    return upload_ts_dir, temp_ts_dir, download_ts_dir, stamp, in_filepath, \
        temp_filepath, out_filepath

def QP(in_filepath, temp_filepath, out_filepath):
    # run midi to csv
    midi_to_csv(in_filepath, temp_filepath)
    print("Creating temp midicsv file at ", temp_filepath)

    # prepping midicsv data for qsys
    print("Preprocessing Data")
    tracklist, keysig = preprocess(temp_filepath)

    print("Performing Qupdate")
    #tracklist = quantum_update(tracklist)

    # Re-writing csv
    print("Updating CSV")
    write_output(temp_filepath, tracklist)

    csv_to_midi(temp_filepath, out_filepath)
    print("Output at", out_filepath)

def create_timestamp_dir(base_path):
    stamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    timedir = os.path.join(base_path, stamp )
    os.makedirs(timedir)
    return timedir, stamp

def swap_extension(path, ext):
    pre, _ = os.path.splitext(path)
    return pre + ext

def delayed_delete(delay, paths):
    print("Started")
    sleep(delay)
    for path in paths:
        try:
            shutil.rmtree(path)
            print("Deleted", path)
        except Exception as e:
            pass
    return
