#!/usr/bin/env python
from distutils.core import setup
import os

scripts=['printedQr']
if os.name is not "posix":
    if os.name is "nt":
        import py2exe
    shutil.copyfile('digenpy','digenpy.py')
    shutil.copyfile('digenpy-gtk','digenpy-gtk.py')
    shutil.copyfile('digenpy-gtk','digenpy-gtk.py')
    scripts=['printedQr.py']

opts = {
    "py2exe": {
        'packages': ['printedQr_'],
    }
}

setup(
    name='printedQr',
    version='0.4',
    description='Print qr codes in Stl or scad',
    author='David Francos Cuartero',
    author_email='me@davidfrancos.net',
    windows = [{"script": "printedQr.py" }],
    console = [{"script": "printedQr.py" }],
    url='http://github.com/dlabs-co/printedQr',
    download_url='http://github.com/dlabs-co/printedQr',
    license='GPL2',
    requires=['qrcode'],
    mantainer='David Francos Cuartero (XayOn)',
    mantainer_email='dfrancos@dlabs.co',
    long_description="Print qr codes in stl or scad",
    packages=['printedQr_'],
    scripts=scripts,
    entry_points="""
        [console_scripts]
        printedQr = printedQr_.printedQr:execute
    """,
    options=opts,
)
