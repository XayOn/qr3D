from flask import Flask, render_template, make_response, request, current_app, Response
from printedQr_ import printedQr
import os
import subprocess
import tempfile

app = Flask(__name__)
app.config['DEBUG'] = True


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/getQr/<text>/<scale>', methods=['GET', 'POST'])
def getQr(text, scale):
    qr = printedQr.QRGen(scale, text)
    qr.make_qr()
    return qr.make_jscad()

@app.route('/getQrScad/<text>/<scale>', methods=['GET', 'POST'])
def getQrScad(text, scale):
    qr = printedQr.QRGen(scale, text)
    qr.make_qr()
    return Response(
        qr.make_scad(),
        mimetype="text/plain",
        headers={"Content-Disposition":"attachment;filename=printedqr.scad"}
    )

def server():
    """ Main server, will allow us to make it wsgi'able """
    app.run(host='0.0.0.0', port=8022)

if __name__ == "__main__":
    server()
