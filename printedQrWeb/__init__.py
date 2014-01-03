from flask import Flask, render_template, make_response, request
from printedQr_ import printedQr
import os
import subprocess
import tempfile

app = Flask(__name__)
app.config['DEBUG'] = True


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/getQr', methods=['POST'])
def getQr():
    text = request.form['text']
    scale = request.form['scale']
    qr = printedQr.QRGen(scale=scale, data=text)

    with tempfile.NamedTemporaryFile(dir="/var/www/digenpy/static/", delete=False) as file_:
        file_.write(qr.make_scad())
        with open("/tmp/openscad_log", 'w') as none:
            subprocess.call(
                [
                    "openscad", file_.name,
                    "-o", file_.name + ".stl"
                ], stdout=none, stderr=none
            )
        return file_.name.replace('/var/www/digenpy', '') + ".stl"

def server():
    """ Main server, will allow us to make it wsgi'able """
    app.run(host='0.0.0.0', port=8022)

if __name__ == "__main__":
    server()
