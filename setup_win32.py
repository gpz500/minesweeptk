from distutils.core import setup
import py2exe

setup( windows = [{
    "script": "minesweeptk.py",
    "icon_resources": [ ( 1, "bomb.ico" ) ] }] )
