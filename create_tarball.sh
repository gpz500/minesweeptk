#!/bin/bash
mkdir Minesweeptk
cp minesweeper.py Minesweeptk
cp minesweeptk.py Minesweeptk
cp bomb.png Minesweeptk
cp *.gif Minesweeptk
tar -cf Minesweeptk.tar Minesweeptk
gzip Minesweeptk.tar
