\:floppy_disk\: QR3D
--------------------

.. image:: http://i.imgur.com/ezLmsVU.png

Cool CLI tool to easily create STL/OpenSCAD files for QR codes
with specified text.

.. contents:: :local:

What can be this used for
++++++++++++++++++++++++++

This allows you to print any `QR Code <https://en.wikipedia.org/wiki/QR_code>`_
with a 3D printer.

That can be useful for:

    - Embedding in openscad objects for authorship tagging
    - Strange 3Dprinted visit cards
    - Cool geeky-makey stuff

Supported formats
=================

QR3D Outputs currently the following formats:

    - OpenSCAD
    - JScad
    - STL (requires openscad installed)


Usage
+++++

::

		Usage: qr3d [OPTIONS]

		  Qr3D - Create nice qr codes in jscad, scad or stl

		Options:
		  --scale INTEGER    QR code size scale
		  --filename TEXT    filename
		  --text TEXT        Text
		  --fileformat TEXT  File format [stl|scad|jscad]
		  --help             Show this message and exit.


Example use:

::

    qr3d --scale 4 --filename foo.stl --fileformat stl --text \
            "http://www.davidfrancos.net"

Have a look at a result STL in github's stl viewer `here <sample.stl>`_.


Thanks
++++++

I'd like to give a special thanks to Feliprint, who made the first
print with this tool (the one documented on the photo!)
