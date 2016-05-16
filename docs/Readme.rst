qr3D
====

Ever wanted to have your custom QR code engraved?
++++++++++++++++++++++++++++++++++++++++++++++++++

With qr3D you can easily generate your own openscad/stl/jscad 3D qr codes.
Just ready for your 3D printer, or to add it to your designs!

As an example use, you could attach it with openscadto your printed
pieces with a link on it!

.. warning::

    It currently prints on only one single color, so you'll need to paint the
    surface with another color or change colors in mid-print


Example output
--------------

After printing with a prusa i3, this is the result
(thanks to feliprint for the print! ;-) )

.. image:: /docs/qr.png


Cli Usage
---------

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

    qr3d --scale 4 --filename foo.stl --fileformat stl --text "http://www.davidfrancos.net"

You can see its output `here </docs/sample.stl>`_.
