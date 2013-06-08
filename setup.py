#!/usr/bin/env python
from distutils.core import setup
import os

if os.name is not "posix":
    if os.name is "nt":
        import py2exe

opts = {
    "py2exe": {
        'packages': ['printedQr'],
    }
}

setup(
    name='printedQr',
    version='0.1',
    description='Print qr codes in Stl or scad',
    author='David Francos Cuartero',
    author_email='me@davidfrancos.net',
    url='http://github.com/dlabs-co/printedQr',
    download_url='http://github.com/dlabs-co/printedQr',
    license='GPL2',
    requires=['qrcode'],
    mantainer='David Francos Cuartero (XayOn)',
    mantainer_email='dfrancos@dlabs.co',
    long_description="Print qr codes in stl or scad",
    packages=['printedQr'],
    entry_points="""
        [console_scripts]
        calentic = calentic.server:server
        calentic_scrappery = calentic.scrappery:main
    """,
    options=opts,
)
