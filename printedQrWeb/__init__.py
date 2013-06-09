from flask import Flask, render_template, Response
from printedQr_ import printedQr

app = Flask(__name__)
app.config['DEBUG'] = True


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/getQr/<text>/<scale>')
@app.route('/getQr/<text>')
def getQr(text, scale=4):
    qr = printedQr.QRGen(scale=scale, data=text)
    qr.make_qr()
    return Response(qr.make_scad(), mimetype='application/octet/stream')


def server():
    """ Main server, will allow us to make it wsgi'able """
    app.run(host='0.0.0.0', port=8022)

if __name__ == "__main__":
    server()
