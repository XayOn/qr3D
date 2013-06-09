#!/usr/bin/env python
# For some reason, building exes with py2exe doesnt work right now.
from setuptools import setup
from distutils.command.install import INSTALL_SCHEMES
import os

for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']

data_files = []

for dirpath, dirnames, filenames in os.walk('printedQrWeb'):
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'):
            del dirnames[i]
    if filenames:
        data_files.append(
            [dirpath, [os.path.join(dirpath, f) for f in filenames]]
        )

setup(
    name='PrintedQrWeb',
    version='0.0.2',
    description='PrintedQr Web interface',
    url='http://printerqr.dlabs.co/',
    download_url='http://printerqr.dlabs.co',
    license='GPL2',
    requires=['PrintedQr'],
    classifiers=[
        'Development Status :: 4 - Beta',
    ],
    long_description="PrintedQr web interface",
    packages=['printedQrWeb'],
    data_files=data_files,
    package_data={
        'printedQrWeb': [
            'static/'
            'templates/'
        ]
    },
    entry_points="""
        [console_scripts]
        printedQrWeb = printedQrWeb:server
    """
)
