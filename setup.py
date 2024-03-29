import os, glob, shutil, sys

from Minesweeptk import APP_NAME
from minesweeper import VERSION
AUTHOR = 'Alessandro Morgantini'
AUTHOR_EMAIL = 'gpz500@technologist.com'
URL = 'https://www.morgantini.org/'
DOC_FILES = [ 'LICENSE', 'changeslog.txt', 'README.md' ]
GIF_FILES = glob.glob( '*.gif' )
PY_FILES = [ 'minesweepertest.py', 'Minesweeptk.py' ]
ICO_FILES = [ 'bomb.ico', 'bomb.icns' ]
I18N_FILES = [ 'Makefile', 'it.po', 'en.po', 'ja.po' ]


def ArchiveDir( dirpath, archname ):
    """Archive a whole directory in a zip file.
    
    dirpath:    the pathname of directory to archive
    archname:   the pathname of destination dir
    
    WARNING: it overwrites every existing archive, no append!
    """
    import zipfile

    print( "Create", archname )
    archive = zipfile.ZipFile( archname, "w", zipfile.ZIP_DEFLATED )

    print( "Archive", dirpath + os.sep )
    archive.write( dirpath )
    
    for dir, subdirs, files in os.walk( dirpath ):
        for subdir in subdirs:
            sdname = os.path.join( dir, subdir )
            print( "Archive", sdname + os.sep )
            archive.write( sdname )
        for file in files:
            fname = os.path.join( dir, file )
            print( "Archive", fname )
            archive.write( fname )
    
    archive.close()    
    


# Initial cleaning
if os.path.isdir( 'dist' ):
    shutil.rmtree( 'dist' )
if os.path.isdir( 'build' ):
    shutil.rmtree( 'build' )

if "py2exe" in sys.argv:

    # py2exe
    assert sys.platform == "win32", "You must be on Windows to run this!"
    import py2exe

    py2exe.freeze(
        windows = [ {
            "script": APP_NAME + ".py",
            'dest_base': APP_NAME,
            "icon_resources": [ ( 0, "bomb.ico" ) ]
        } ],
        data_files = [
            ( "locale\\it\\LC_MESSAGES\\", [ "locale\\it\\LC_MESSAGES\\Minesweeptk.mo" ] ),
            ( "locale\\en\\LC_MESSAGES\\", [ "locale\\en\\LC_MESSAGES\\Minesweeptk.mo" ] ),
            ( "locale\\ja\\LC_MESSAGES\\", [ "locale\\ja\\LC_MESSAGES\\Minesweeptk.mo" ] )
        ],
        version_info = {
            'version': VERSION,
            'description': 'A cross-platform Minesweeper game clone, implemented in Pyhon and Tcl/Tk.',
            'product_name': APP_NAME,
            'product_version': VERSION,
            'copyright': 'Copyright © 2012-2023 Alessandro Morgantini. Released under the terms of GNU GPL Version 2.'
        }
    )
    
    # Put in dist *.txt files
    for file in DOC_FILES:
        shutil.copy( file, 'dist' )
        
    # Put in dist *.gif files
    for file in GIF_FILES:
        shutil.copy( file, 'dist' )

    # Create the .zip file    
    shutil.move( 'dist', APP_NAME )
    ArchiveDir( APP_NAME, APP_NAME + "-Win32-AMD64-" + VERSION + ".zip" )
    shutil.rmtree( APP_NAME )

    
elif "py2app" in sys.argv:


    # py2app
    assert sys.platform == 'darwin', 'You must be on Mac OS X to run this!'
    from setuptools import setup
    
    # Extra files to include in the distribution
    extraFiles = GIF_FILES
    extraFiles.append( ( "locale/it/LC_MESSAGES", [ "locale/it/LC_MESSAGES/Minesweeptk.mo" ] ) )
    extraFiles.append( ( "locale/en/LC_MESSAGES", [ "locale/en/LC_MESSAGES/Minesweeptk.mo" ] ) )
    extraFiles.append( ( "locale/ja/LC_MESSAGES", [ "locale/ja/LC_MESSAGES/Minesweeptk.mo" ] ) )
    
    setup(
        app = [ APP_NAME + ".py" ],
        data_files = extraFiles,
        options = {
            'py2app': {
                'iconfile': 'bomb.icns'
            }
        },
        setup_requires = [ 'py2app' ]
    )

    # Copy binary files for Tcl/Tk
    # Workaround for py2app issue: https://github.com/ronaldoussoren/py2app/issues/202
    import tkinter
    from pathlib import Path
    root = tkinter.Tk()
    root.overrideredirect(True)
    root.withdraw()
    tcl_dir = Path(root.tk.exprstring('$tcl_library'))
    tk_dir = Path(root.tk.exprstring('$tk_library'))
    root.destroy()

    os.makedirs(f"dist/{APP_NAME}.app/Contents/lib")
    shutil.copytree(tk_dir, f"dist/{APP_NAME}.app/Contents/lib/{tk_dir.parts[-1]}")
    shutil.copytree(tcl_dir, f"dist/{APP_NAME}.app/Contents/lib/{tcl_dir.parts[-1]}")

    # Put in dist *.txt files
    for file in DOC_FILES:
        shutil.copy( file, 'dist' )
    
    # Create the .dmg file
    dirname = APP_NAME + " v" + VERSION
    shutil.move( 'dist', dirname )
    dmgname = APP_NAME + "-macOS-x86_64-" + VERSION
    cmdline = "hdiutil create " + dmgname + " -srcfolder \"" + dirname + "\""
    os.system( cmdline )
    shutil.rmtree( dirname )
    
else:

    # Plain setup.py file
    extraFiles = DOC_FILES
    extraFiles.extend( GIF_FILES )
    extraFiles.extend( PY_FILES )
    extraFiles.extend( ICO_FILES )
    extraFiles.extend( I18N_FILES )
    
    # Create a MANIFEST.in file
    f = open( 'MANIFEST.in', 'w' )
    for file in extraFiles:
        print( "include", file, file = f )
    f.close()

    
    from distutils.core import setup

    setup(
        name = APP_NAME,
        version = VERSION,
        url = URL,
        author = AUTHOR,
        author_email = AUTHOR_EMAIL,
        py_modules = [ 'minesweeper', 'ttk' ]
    )

