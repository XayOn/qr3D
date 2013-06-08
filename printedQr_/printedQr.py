#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
    text2QrStl - Convert your QR codes to stl
"""

import qrcode
import sys
import os
import argparse
import subprocess


class QRGen(object):
    """
        Main class, generates qr code and scad
    """
    def __init__(self, scale=False):
        self.scale = scale
        if not self.scale:
            self.scale = 4
        self.data = ""
        self.qr_base = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )

    def make_qr(self):
        self.qr_base.add_data(sys.argv[1])
        self.qr_base.make(fit=True)

    def make_scad(self):
        result = "qr_size=" + str(self.qr_base.modules_count) + ";"
        result += 'module qrcode() {\n'
        for row in range(self.qr_base.modules_count):
            for column in range(self.qr_base.modules_count):
                if self.qr_base.modules[row][column]:
                    result += '    translate([%(x)s, %(y)s, 0])' % {
                        'x': 1 * column - self.qr_base.modules_count / 2,
                        'y': - 1 * row + self.qr_base.modules_count / 2
                    }
                    result += 'cube([%s, %s, 1]);\n' % ("1", "1")
        result += '}\n'
        result += "scale([%s,%s,%s]){ union(){ qrcode(); " \
            % (self.scale, self.scale, self.scale) + \
            "translate([-10, -10, -1]) cube([qr_size,qr_size,1]); }}"
        return result


def argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', dest="filename",
                        help='File to save it')
    parser.add_argument('data', metavar='N', type=str,
                        nargs='+', help='Qr data')
    parser.add_argument('--scale', dest="scale",
                        help='Scale the qr code', default=False)
    parser.add_argument('--format', dest="format",
                        help='Format to save it on, \
                            stl may not work on windows',
                        choices=["stl", "scad"],
                        default="scad")
    return parser.parse_args()


def execute():
    args = argument_parser()
    qr = QRGen(args.scale)
    qr.make_qr()
    if args.format == "stl":
        if not args.filename:
            print "Sorry, filename is required to export stl file"
            sys.exit(1)

    if args.filename:
        with open(args.filename, "w") as file_:
            file_.write(qr.make_scad())
        sys.platform.startswith('win')

        openscad_binary = "openscad"

        if sys.platform.startswith('win'):

            window_paths = [
                os.environ["ProgramFiles"],
                os.environ["ProgramFiles(x86)"],
                os.environ["ProgramW6432"]
            ]
            for path in window_paths:
                openscad_binary = os.path.join(
                    path,
                    "OpenScad",
                    openscad_binary + ".exe"
                )
                if os.path.isfile(openscad_binary):
                    break
            if not os.path.isfile(openscad_binary):
                print "Sorry, could not find openscad in your system"
                sys.exit(1)

        subprocess.Popen(
            [
                openscad_binary, args.filename,
                "-o", args.filename + ".stl"
            ]
        )
    else:
        print qr.make_scad()

if __name__ == "__main__":
    execute()
