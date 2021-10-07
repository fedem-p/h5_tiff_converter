#!/usr/bin/env python3

import os
from setuptools import setup
from setuptools import find_packages

#get long description

with open("README.md") as f:
    long_description = f.read()

# package configuration - for reference see:
# https://setuptools.readthedocs.io/en/latest/setuptools.html#id9
setup(
    name='H5_2_Tiff_Converter',
    description='a flexible converter to extract tiff files from h5',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version='0.1',
    author='Federico Puppo',
    author_email='federico.puppo@tum.de',
    url='https://github.com/fedem-p/h5_tiff_converter',
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.7",
    license='MIT',
    zip_safe=False,
    entry_points={
        'console_scripts': ['H5_2_Tiff_Converter=H5_2_Tiff_Converter.entry_points:h5_2_tiff_converter'],
    },
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.7',
        'Natural Language :: English',
    ],
    keywords='H5 Tiff Converter'
)