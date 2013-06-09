#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
    text2QrStl - Convert your QR codes to stl
"""

import qrcode
import logging
import sys
import os
import argparse
import subprocess


class QRGen(object):
    """
        Main class, generates qr code and scad
    """
    def __init__(self, scale=False, data=""):
        """
            Setup essentials
        """
        self.scale = scale
        if not self.scale:
            self.scale = 4
        self.data = data
        self.qr_base = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )

    def make_qr(self):
        """
            Create the qr code
            This will return an array with all the dots,
            in true/false status
        """
        self.qr_base.add_data(self.data)
        self.qr_base.make(fit=True)

    def make_scad(self):
        """
            Generate the scad content
            I took part of this code (translate and cubes)
            from qr2scad, from l0b0: https://github.com/l0b0/qr2scad
        """
        result = "qr_size=" + str(self.qr_base.modules_count) + ";"
        result += 'module qrcode() {\n'
        for row in range(self.qr_base.modules_count):
            for column in range(self.qr_base.modules_count):
                if self.qr_base.modules[row][column]:
                    result += '    translate([%(x)s, %(y)s, 0]) ' % {
                        'x': 1 * column - self.qr_base.modules_count / 2,
                        'y': - 1 * row + self.qr_base.modules_count / 2
                    }
                    result += 'cube([0.99, 0.99, 1]);\n'
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


def get_openscad_windows_binary():
    """
        Iterate trough common paths to try
        to find openscad
    """
    window_paths = [
        os.environ["ProgramFiles"],
        os.environ["ProgramFiles(x86)"],
        os.environ["ProgramW6432"]
    ]
    for path in window_paths:
        openscad_binary = os.path.join(
            path,
            "OpenScad",
            "openscad.exe"
        )
        if os.path.isfile(openscad_binary):
            break
    if not os.path.isfile(openscad_binary):
        print "Sorry, could not find openscad in your system"
        sys.exit(1)
    return openscad_binary


def execute():
    """
        Execute the stuff
    """
    # Init logger
    logging.basicConfig(level=logging.INFO)
    log = logging.getLogger('printedQr')
    # Get args
    args = argument_parser()
    # Generate qr
    qr = QRGen(args.scale, sys.argv[1])
    qr.make_qr()
    # Make some checks
    if args.format == "stl":
        if not args.filename:
            print "Sorry, filename is required to export stl file"
            sys.exit(1)

    if args.filename:
        with open(args.filename + ".scad", "w") as file_:
            file_.write(qr.make_scad())
        openscad_binary = "openscad"

        if sys.platform.startswith('win'):
            openscad_binary = get_openscad_windows_binary()

        log.info("Converting file to STL, please wait a few mintutes")

        with open(os.devnull, 'w') as none:
            subprocess.call(
                [
                    openscad_binary, args.filename + ".scad",
                    "-o", args.filename + ".stl"
                ], stdout=none, stderr=none
            )

        log.info("Conversion finished, you'll find your stl in %s"
                 % (args.filename + ".stl"))
    else:
        print qr.make_scad()

if __name__ == "__main__":
    execute()
