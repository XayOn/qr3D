#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Convert qr codes to jscad, openscad and stl"""

import qrcode
import click
import subprocess
from jinja2 import Environment


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
    def __init__(self, filename, scale=4, data=""):
        self.scale = scale
        self.filename = filename
        self.qr_base = qrcode.QRCode(
            version=1, error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10, border=4,
        )
        self.qr_base.add_data(data)
        self.qr_base.make(fit=True)
        self.qr_size = self.qr_base.modules_count

    @property
    def cubes(self):
        """ Calculate all cubes for the qr code """
        cubes = []
        for row in range(self.qr_size):
            for column in range(self.qr_size):
                if not self.qr_base.modules[row][column]:
                    continue
                cubes.append([1 * column - self.qr_size / 2,
                              - 1 * row + self.qr_size / 2])
        return cubes

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
            [-10, -10, -1])

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
        translate([-10, -10, -1]) cube([qr_size,qr_size,1]);
    }
}"""


@click.command()
@click.option('--scale', default=4, help="QR code size scale")
@click.option('--filename', default='/dev/stdout', help="filename")
@click.option('--text', help="Text")
@click.option('--fileformat', default="scad",
              help="File format [stl|scad|jscad]")
def execute(scale, filename, fileformat, text):
    """Execute the stuff"""
    format_ = fileformat
    qrcodew = QRCode(filename=filename, scale=scale, data=text)

    if fileformat == "stl":
        format_ = "scad"

    with open(qrcodew.filename, 'w') as file_:
        file_.write(getattr(qrcodew, format_)())

    if fileformat == "stl":
        subprocess.check_call([
            "openscad", qrcodew.filename, "-o", qrcodew.filename])
