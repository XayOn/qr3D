#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Qr3D - Create nice qr codes in jscad, scad or stl

Usage: qr3d --scale <INTEGER> --filename <FILENAME> --text <TEXT> --fileformat <FORMAT>

Options:
  --scale INTEGER    QR code size scale
  --filename TEXT    filename
  --text TEXT        Text
  --fileformat TEXT  File format [stl|scad|jscad] [default: scad]
  --help             Show this message and exit.
"""

from itertools import permutations
import subprocess
import qrcode
from jinja2 import Environment
from docopt import docopt


def render_template(func):
    """ Render a jinja2 template with the qr code as function """
    def render(*args):
        """ Decorator """
        template = func(*args)
        result = Environment().from_string(template).render(q=args[0])
        return result

    return render


class QRCode(object):
    """Main class, generates qr code and scad"""
    def __init__(self, filename, scale=4, text=""):
        self.scale = scale
        self.filename = filename
        self.qr_base = qrcode.QRCode(
            version=1, error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10, border=4,
        )
        self.qr_base.add_data(text)
        self.qr_base.make(fit=True)
        self.qr_size = self.qr_base.modules_count
        self.qr_half = int(self.qr_size / 2)

    @property
    def cubes(self):
        """ Calculate all cubes for the qr code """
        for row, column in permutations(range(self.qr_size), 2):
            if not self.qr_base.modules[row][column]:
                continue
            yield [1 * column - self.qr_size / 2,
                   - 1 * row + self.qr_size / 2]

    @render_template
    def jscad(self):
        """ Format qr in jscad """
        return """
qr_size = {{q.qr_size}};

function main(){
{
    return union(
        {%for cube in q.cubes %}
            cube({size:[0.99, 0.99, 1]}).translate(
                [{{cube[0]}}, {{cube[1]}}, 0]),
        {% endfor %}

        cube([{{q.qr_size}}, {{q.qr_size}}, 1]).translate(
            [-{{q.qr_half}}, -{{q.qr_half}}, -1])

    ).scale([{{q.scale}}, {{q.scale}}, {{q.scale}}]);
}
}"""

    @render_template
    def scad(self):
        """ Format qr in openscad """
        return """
qr_size={{q.qr_size}};
module qrcode(){
    {%for cube in q.cubes %}
    translate([{{cube[0]}}, {{cube[1]}}, 0]) cube([0.99, 0.99, 1]);{%endfor%}
}
scale([{{q.scale}},{{q.scale}},{{q.scale}}]){
    union(){
        qrcode();
        translate([-{{q.qr_half}}, -{{q.qr_half}},
                    -1]) cube([{{q.qr_size}},{{q.qr_size}},1]);
    }
}"""


def execute():
    """Qr3D - Create nice qr codes in jscad, scad or stl """
    opts = docopt(__doc__, version="0.0.1")
    fileformat = opts.pop('--fileformat')
    qrcodew = QRCode(**{b[2:]: val for b, val in opts.items()})

    format_ = fileformat
    if fileformat == "stl":
        format_ = "scad"

    with open(qrcodew.filename, 'w') as file_:
        file_.write(getattr(qrcodew, format_)())

    if fileformat == "stl":
        subprocess.check_call([
            "openscad", qrcodew.filename, "-o", qrcodew.filename])
