#!/bin/bash
rm -rf build
rm -rf dist
python setup_macosx.py py2app
