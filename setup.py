#!/usr/bin/env python
from distutils.core import setup

setup(
    name='printer',
    version='0.4',
    description='Print qr codes in Stl or scad',
    author='David Francos Cuartero',
    author_email='me@davidfrancos.net',
    windows=[{"script": "printer.py"}],
    console=[{"script": "printer.py"}],
    url='http://github.com/dlabs-co/printer',
    download_url='http://github.com/dlabs-co/printer',
    license='GPL2',
    requires=['qrcode', 'click'],
    mantainer='David Francos Cuartero (XayOn)',
    mantainer_email='dfrancos@dlabs.co',
    long_description="Print qr codes in stl or scad",
    packages=['qr_printer'],
    entry_points="""
        [console_scripts]
        printer = qr_printer.printer:execute
    """,
)
