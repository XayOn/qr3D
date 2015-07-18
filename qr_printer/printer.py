#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Convert qr codes to jscad, openscad and stl"""

import qrcode
import click
import logging
import subprocess
from tempfile import NamedTemporaryFile
from qr_printer.openscad import get_openscad_path


class QRCode(object):
    """Main class, generates qr code and scad"""
    def __init__(self, filename, scale=4, data=""):
        """Setup essentials"""
        self.scale = scale
        self.filename = filename
        self.qr_base = qrcode.QRCode(
            version=1, error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10, border=4,
        )
        self.qr_base.add_data(data)
        self.qr_base.make(fit=True)

    def stl(self):
        """Convert to sqtl."""
        openscad_binary = get_openscad_path()
        with NamedTemporaryFile() as file_:
            subprocess.check_call([
                openscad_binary, file_.name, "-o", self.filename])

    def get_cubes(self, cube, edge):
        """Calculate all cubes for the qr code"""
        res = ""
        for row in range(edge):
            for column in range(edge):
                if self.qr_base.modules[row][column]:
                    res += cube.format(
                        1 * column - edge / 2,
                        - 1 * row + edge / 2
                    )

        return res

    def format_results(self, result, cube):
        """Return result formatted"""
        edge = self.qr_base.modules_count
        return result.format(
            sc=self.scale,
            qr_size=self.qr_base.modules_count,
            cont=self.get_cubes(cube, edge)
        )

    @property
    def jscad(self):
        """Generate the jsscad content"""
        return self.format_results(
            '\n'.join([
                "qr_size={qr_size};", 'function main(){{ return union(',
                "{cont}",
                "cube([qr_size,qr_size,1]).translate([-10, -10, -1])",
                ').scale([{sc},{sc},{sc}]);}}']),
            'cube({{size:[0.99, 0.99, 1]}}).translate([{}, {}, 0])\n')

    @property
    def scad(self):
        """Generate the scad content"""
        return self.format_results(
            '\n'.join([
                "qr_size={qr_size}", 'module qrcode() {{\n', '{cont}}}\n',
                "scale([{sc},{sc},{sc}]){{ union(){{ qrcode(); ",
                "translate([-10, -10, -1]) cube([qr_size,qr_size,1]); }}"]),
            'translate([{}, {}, 0])\n cube([0.99, 0.99, 1]);\n')


@click.command()
@click.option('--scale', default=4, help="QR code size scale")
@click.option('--filename', default='/dev/stdout', help="filename")
@click.option('--text', help="Text")
@click.option('--fileformat', help="File format [stl|scad|jscad]")
def execute(scale, filename, fileformat, text):
    """Execute the stuff"""
    qrcodew = QRCode(filename=filename, scale=scale, data=text)

    convert_to_stl = False
    if fileformat == "stl":
        fileformat = "scad"
        convert_to_stl = True

    with open(qrcodew.filename, 'w') as file_:
        file_.write(getattr(qrcodew, fileformat))

    if convert_to_stl:
        qrcodew.stl()
