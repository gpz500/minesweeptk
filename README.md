Minesweeptk: a cross-platform Minesweeper game clone, implemented in Pyhon and Tcl/Tk
=====================================================================================

Minesweeptk is an implementation of the well known [Minesweeper game][1] written
in Python and using the Tcl/Tk graphical tool kit. It works on every system
where there is Python 3.x with Tcl/Tk installed.

Tested on Windows, Linux and macOS.

Localization effort
-------------------

I'm in the effort of localizing Minesweeptk.py to several languages and, to do
it, I have used the Python port of GNU gettext library
(<https://docs.python.org/3/library/gettext.html>).
Only English, Italian and Japanese are available so far.

In order to compile GNU gettext binary files (\*.mo) from input files (\*.po),
needed to run Minesweeptk in localized language, run the command

    $ make
    
(GNU gettext and GNU make required). The resulting files will be put to
./locale/&lt;locale_name>/LC_MESSAGES/Minesweeptk.mo.

Anyone who would like to translating the Minesweeptk UI to a new language can
contact me. Or, if accustomed to Github, he/she can fork
[this repository on Github][2], compose the .po file and make a Pull Request for
that.

minesweeper Python module
-------------------------

minesweeper.py is a module to implement the Minsweeper Windows game.
It defines two classes:

- Cell, which implements a single cell on the table
- Game, which implements a game as a matrix of Cell instances

Please read the *.py files to obtain more info.

Build for Windows
-----------------

To build the Windows executable Minesweeptk.exe and its distribution archive
from the source tree (Minesweeptk-X.Y), run the following command:

    C:\Minesweeptk-X.Y>python setup.py py2exe
    
Note: you need py2exe from https://www.py2exe.org/. Tested with Python 3.11 and
py2exe 0.13.0.0.

Build for macOS
---------------

To build the Minesweeptk application bundle for macOS, from the source tree
(Minesweeptk-X.Y), run the following command:

    $ python3 setup.py py2app
    
Note: you need py2app from https://py2app.readthedocs.io/. Tested with Python 3.11
and py2app 0.28.6.
    
Install (sources)
-----------------

Just to play, you don't have to install anything. It is sufficient opening a
terminal and running the followings commands from this folder (Minesweeptk-X.Y):

    $ python3 minesweeper.py         <-- text based game
        or
    $ python3 Minesweeptk.py         <-- Tcl/Tk based GUI game

In order to install minesweeper module on your system, so you can use
it in your own applications, run this command as superuser:

    # python setup.py install
    
Install (macOS)
------------------

Just drag'n'drop Minesweeptk application bundle in your Applications folder, and
then double click it.
Note that Minesweeptk app isn't notarized so, the first time you open
it, you have to CTRL+click on it and then choose Open.

Install (Windows)
-----------------

There is no automatic setup program, just a .zip archive: double click the
Minesweeptk.exe file in the extracted folder.

Screenshots
-----------

On Windows:  
![On Windows](screenshots/Windows%20screenshot.png)

On Linux:  
![On Linux](screenshots/Ubuntu%20screenshot.png)

On Macintosh:   
![On Macintosh](screenshots/Mac%20OS%20X%20screenshot.png)

Credits
-------

Thanks to Roan Soldaini for the Japanese translation.

Contacts
--------

Please refer any bugs and/or suggests to
    Alessandro Morgantini <gpz500@technologist.com>,
or submit a comment to this blog post:
    <https://gpz500.wordpress.com/2012/02/07/e-ora-di-sminare-il-campo/>.
    
[1]: https://en.wikipedia.org/wiki/Minesweeper_%28video_game%29
[2]: https://github.com/gpz500/minesweeptk

