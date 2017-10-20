from flask import Flask, request, send_from_directory
from flask import safe_join, redirect, url_for
from werkzeug.utils import secure_filename
import os

if not os.path.exists('uploads'):
    os.makedirs('uploads')

if not os.path.exists('downloads'):
    os.makedirs('downloads')

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
DOWNLOAD_FOLDER = 'downloads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

@app.route("/", methods=['GET','POST'])
def serve_main():
    if request.method == 'GET':
        return app.send_static_file('index.html')

    elif request.method == 'POST':
        if 'midi_file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        f = request.files['midi_file']
        filename = secure_filename(f.filename)
        in_filepath = safe_join(UPLOAD_FOLDER, filename)
        out_filepath = safe_join(DOWNLOAD_FOLDER, filename)
        f.save(in_filepath)





        return redirect(url_for('uploaded_file', filename=filename))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/downloads/<filename>')
def ready_file(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename)
