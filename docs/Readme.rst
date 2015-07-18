printedQr
=========

Qr code message generator in 3D, ready to be printed by a 3D printer

With this, you can print a necklace, or some message to be left on your 3D printer, phisically.

.. warning::
    It currently prints on only one single color, so you'll need to paint the surface with another
    color.


Example output
--------------

After printing with a prusa i3, this is the result (thanks to feliprint for the print! ;-) )

.. image:: /docs/qr.png

Cli Usage
---------

::

    Usage: qr_printer [OPTIONS]

      Execute the stuff

    Options:
      --scale INTEGER    QR code size scale
      --filename TEXT    filename
      --text TEXT        Text
      --fileformat TEXT  File format [stl|scad|jscad]
      --help             Show this message and exit.
