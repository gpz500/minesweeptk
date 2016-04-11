Minesweeptk: a cross-platform Minesweeper game clone, implemented in Pyhon and Tcl/Tk
=====================================================================================

Minesweeptk is an implementation of the well known [Minesweeper game][1] written
in Python and using the Tcl/Tk graphical tool kit. It works in every system
where there are Python 2.x or Python 3.x (Python 3.x version is in a separate
branch) with Tcl/Tk installed.

Tested on Windows, Linux and Mac OS X.

Localization effort
-------------------

I'm in the effort of localizing Minesweeptk.py to several languages and, to do
it, I have used the Python port of GNU gettext library
(<https://docs.python.org/2.7/library/gettext.html>).
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
    
Note: you need py2exe from http://www.py2exe.org/.

Build for Mac OS X
------------------

To build the Minesweeptk application bundle for Mac OS X, from the source tree
(Minesweeptk-X.Y), run the following command:

    $ python setup.py py2app
    
Note: you need py2app from https://pythonhosted.org/py2app/.
    
Install (sources)
-----------------

Just to play, you don't have to install anything. It is sufficient opening a
terminal and running the followings commands from this folder (Minesweeptk-X.Y):

    $ python minesweeper.py         <-- text based game
        or
    $ python Minesweeptk.py         <-- Tcl/Tk based GUI game

In order to install minesweeper module on your system, so you can use
it in your own applications, run this command as superuser:

    # python setup.py install
    
Install (Mac OS X)
------------------

Just drag'n'drop Minesweeptk application bundle in your Applications folder, and
then double click it.

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
    <http://gpz500.wordpress.com/2012/02/07/e-ora-di-sminare-il-campo/>.
    
[1]: https://en.wikipedia.org/wiki/Minesweeper_%28video_game%29
[2]: https://github.com/gpz500/minesweeptk

