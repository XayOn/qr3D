#!/usr/bin/env python
from distutils.core import setup

setup(
    name='Qr3D',
    version='1.0.1',
    description='Print qr codes in stl, openscad or jscad',
    author='David Francos Cuartero',
    author_email='me@davidfrancos.net',
    url='http://github.com/dlabs-co/Qr3D',
    download_url='http://github.com/XayOn/Qr3D',
    license='GPL2',
    install_requires=['qrcode', 'click', 'jinja2'],
    long_description="Print qr codes in stl or scad",
    packages=['qr3d'],
    entry_points="""
        [console_scripts]
        qr3d = qr3d:execute
    """,
)
