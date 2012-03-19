minesweeper Python 2.x module
=============================

minesweeper is a module to implement the well known Minsweeper Windows game. It
has two classes:

- Cell, which implements a single cell on the table
- Game, which implements a game as a matrix of Cell instances

Plase read the .py files to obtain more info.

Install (sources)
=================

Just to play, you don't have to install anything. It is sufficient open a
terminal and run the followings commands from this folder (Minesweeptk-X.Y):

    $ python minesweeper.py         <-- text based game
        or
    $ python Minesweeptk.py         <-- Tcl/Tk based GUI game

In order to install minesweeper module on your system, so you can use
it in your own applications, run this command as superuser:

    # python setup.py install
    
I'm in the effort of localize to several languages Minesweeptk.py. In order to
compile GNU gettext binary files (*.mo) from input files (*.po) run the command

    $ make
    
(it requires GNU gettext installed). The resulting files will be in
./locale/*/LC_MESSAGES/Minesweeptk.mo
    
Install (Mac OS X)
===================

Just drag'n'drop Minesweeptk application bundle in your Application folder, and
then double click it.

Install (Windows)
=================

There is no automatic setup program, just a .zip archive: double click the
Minesweeptk.exe file in the extracted folder. 

Build for Windows
=================

To build the Windows executable Minesweeptk.exe and its distribution archive
from the source tree (Minesweeptk-X.Y), run the following command:

    C:\Minesweeptk-X.Y> python setup.py py2exe
    
Note: you need py2exe from http://www.py2exe.org/.

Build for Mac OS X
===================

To build the Minesweeper application bundle for Mac OS X, from the source tree
(Minesweeptk-X.Y), run the following command:

    $ python setup.py py2app
    
Note: you need py2exe from http://svn.pythonmac.org/py2app/trunk/doc/index.html.
    
Credits
=======

Thanks to Roan Soldaini for the Japanese translation.

Contacts
========

Please refer any bugs and/or suggests to
    Alessandro Morgantini <gpz500@technologist.com>
    
or submit a comment to this blog post:
    http://gpz500.wordpress.com/2012/02/07/e-ora-di-sminare-il-campo/
    