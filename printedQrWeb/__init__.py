from flask import Flask, render_template, make_response
from printedQr_ import printedQr

app = Flask(__name__)
app.config['DEBUG'] = True


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/getQr/<text>/<scale>')
@app.route('/getQr/<text>')
@app.route('/getQr/<text>/')
def getQr(text, scale=4):
    qr = printedQr.QRGen(scale=scale, data=text)
    qr.make_qr()
    response = make_response(qr.make_scad)
    response.headers['Content-Type'] = 'application/octect-stream'
    response.headers['Content-Disposition'] = 'attachment; filename=Qr' +  \
        text[:3] + '.scad'
    return response


def server():
    """ Main server, will allow us to make it wsgi'able """
    app.run(host='0.0.0.0', port=8022)

if __name__ == "__main__":
    server()
