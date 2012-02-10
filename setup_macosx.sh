#!/bin/bash
rm -rf build
rm -rf dist
python setup_macosx.py py2app
cp license.txt dist
cp changeslog.txt dist
mv dist/minesweeptk.app dist/Minesweeptk.app
mv dist Minesweeptk

