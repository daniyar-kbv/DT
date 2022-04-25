from flask import Flask, request, render_template, url_for, redirect
from werkzeug.utils import secure_filename
import os
import torch
import od_utils

model = torch.hub.load('ultralytics/yolov5', 'custom', path='model/best.pt', force_reload=True)
model.eval()

os.environ['FLASK_APP'] = 'dt'
# os.environ['FLASK_ENV'] = 'prod'
os.environ['FLASK_ENV'] = 'development'
root = os.popen('pwd').read().splitlines()[0]

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = root + '/static'
app.config['MAX_CONTENT_PATH'] = 50000000


@app.route('/home')
def home():
    filename = request.args.get('filename', None)
    print(filename)
    return render_template('index.html', is_file=filename is not None, filename=filename)


@app.route('/detect', methods=['POST'])
def detect():
    f = request.files['file']
    filename = secure_filename(f.filename)
    file_path = f'{app.config["UPLOAD_FOLDER"]}/{filename}'
    f.save(file_path)
    filename = od_utils.process(file_path, model)
    # import time
    # time.sleep(10)
    return redirect(url_for('home', filename=filename))


if __name__ == "__main__":
    app.run()