"""This program implements a personal version of Windows minesweeper game.

It uses the module minesweeper.py which gives two classes:
- Cell, for a single cell
- Game, which is a matrix of Cells."""

__author__ = "Alessandro Morgantini <gpz500@technologist.com>"
__version__ = "$Revision$"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2012 Alessandro Morgantini"
__license__ = "Python"

import os
import Tkinter              # For GUI stuff
import Dialog               # For "Game Over" dialogs
from Tkinter import *       
from ttk import *
import minesweeper          # For the minesweeper game

# The application name
APP_NAME = "Minesweeptk"

# Some i18n
import gettext
gettext.install( APP_NAME, 'locale' )

# Define constants for cells status
CELL_STATUS_ZERO, CELL_STATUS_ONE, CELL_STATUS_TWO, CELL_STATUS_THREE, \
CELL_STATUS_FOUR, CELL_STATUS_FIVE, CELL_STATUS_SIX, CELL_STATUS_SEVEN, \
CELL_STATUS_EIGHT, CELL_STATUS_BOMB, CELL_STATUS_FLAG, CELL_STATUS_QMARK, \
CELL_STATUS_COVERED, CELL_STATUS_PRESSED, CELL_STATUS_BBORD, CELL_STATUS_RBORD, \
CELL_STATUS_CBORD, CELL_STATUS_FALSEN, CELL_STATUS_FALSEP = range( 19 )

# Images to display a cell in every cell status
imagesFilenames = ( 'zero.gif', 'one.gif', 'two.gif', 'three.gif',
                    'four.gif', 'five.gif', 'six.gif', 'seven.gif',
                    'eight.gif', 'bomb.gif', 'flag.gif', 'q_mark.gif',
                    'covered.gif', 'pressed.gif', 'bottombord.gif', 'rightbord.gif',
                    'cornerbord.gif', 'falsenegative.gif', 'falsepositive.gif' )
images = []

# Size of table and number of mines
option = 1
options = [ { "nrows": 9, "ncols": 9, "nmines": 10 },
            { "nrows": 16, "ncols": 16, "nmines": 40 },
            { "nrows": 16, "ncols": 30, "nmines": 99 },
            { "nrows": 16, "ncols": 16, "nmines": 40 } ]

            
# The filename in '~' where to save the current game
SAVE_FILE_NAME = os.path.join( os.path.expanduser( "~" ), ".minesweeptk_save" )

#-------------------------------------------------------------------------------
# A class to save/load persistent data
#-------------------------------------------------------------------------------
class PersistentData:
    """This class implements an interface to manage persistent data."""
    
    def __init__( self, filename ):
        """Initialize the instance with the file name."""
        
        # Init the filename 
        self.filename = filename
        
        # Import pickle module and map as instance variable
        import pickle
        self.pickle = pickle
        
        
    def SaveGame( self, game ):
        """Save the supplied game on file."""
        # Load saved options
        try:
            svdOption, svdOptions = self.LoadOptions()
        except IOError:
            # If the file does'n exist, set default values
            # for custom options
            svdOption = option
            svdOptions = options[ 3 ]
            
        with open( self.filename, "wb" ) as f:
            pck = self.pickle.Pickler( f )
            pck.dump( game )
            pck.dump( svdOption )
            pck.dump( svdOptions )
       
        
    def LoadGame( self ):
        """Load the saved game from file."""
        with open( self.filename, "rb" ) as f:
            unpck = self.pickle.Unpickler( f )
            game = unpck.load()

        return game
            
        
    def SaveOptions( self, option, options ):
        """Save the supplied custom options on file."""
        # Load saved game
        try:
            svdGame = self.LoadGame()
        except IOError:
            # If the file doesn't exist, put an invalid one
            svdGame = "You've never saved any game!"
            
        with open( self.filename, "wb" ) as f:
            pck =  self.pickle.Pickler( f )
            pck.dump( svdGame )
            pck.dump( option )
            pck.dump( options )

        
    def LoadOptions( self ):
        """Load the saved custom options from file."""
        with open( self.filename, "rb" ) as f:
            unpck = self.pickle.Unpickler( f )
            # Read the saved game
            dummy = unpck.load()
            try:
                svdOption = unpck.load()
                svdOptions = unpck.load()
            except EOFError:
                # It's possible open old savings (without options), so,
                # if the file is too short, set default values
                svdOption = option
                svdOptions = options[ 3 ]
        
        return ( svdOption, svdOptions )
        
    


#-------------------------------------------------------------------------------
# A class to implement a single cell
#-------------------------------------------------------------------------------
class CellButton( Tkinter.Label ):
    """CellButton is the widget class which implement a single cell.
    
    It's a class derived from Tkinter.Label, so it is able to visualize
    images. Every single cell is linked to the "real" cell in the
    underlying minesweeper.Game instance."""
    
    # Status value related to mouse pressing on the cell
    UNPRESSED = 0   # Cell non-pressed
    PRESSED   = 1   # Cell pressed with mouse cursor inside the cell
    LEAVED    = 2   # Cell pressed with mouse cursor outdise the cell
    
    def __init__( self, master, ucell ):
        """Initialize a new CellButton instance.
        
        master: the cell master widget, usually the game table
        ucell:  the underlying cell in the minesweeper.Game instance
                which this cell is linked to."""
        
        Tkinter.Label.__init__( self, master )

        # Every cell widget is linked to a "real" cell in the
        # underlying minesweeper.Game instance
        self.ucell = ucell
        
        self[ 'bd' ] = 0    # borderwidth = 0
        row, col = self.ucell.GetCoordinates()
        self.grid( row = row, column = col )
        
        # This is cell status (it identifies which image to show on the cell)
        # starting non-initialized
        self.status = -1
        
        # A variable to manage the press status of the cell
        self.pressed = self.UNPRESSED
        
        # Add a bind tag. This assigns to all cells a common Tk widget class
        tagsList = list( self.bindtags() )
        tagsList.append( self.__class__.__name__ )
        self.bindtags( tuple( tagsList ) )
        
    def Update( self ):
        """Update the cell status from the underlying ucell."""
        ucellSt = self.ucell.GetStatus()
        
        if ucellSt == minesweeper.Cell.COVERED:
            newStatus = CELL_STATUS_COVERED
        elif ucellSt == minesweeper.Cell.FLAG:
            newStatus = CELL_STATUS_FLAG
        elif ucellSt == minesweeper.Cell.Q_MARK:
            newStatus = CELL_STATUS_QMARK
        elif self.ucell.HasMine():
            newStatus = CELL_STATUS_BOMB
        else:
            newStatus = self.ucell.GetNeighborMinesNum()
            
        self._SetStatus( newStatus )
        
        
    def _SetStatus( self, newStatus ):
        """Set the cell display status.
        
        0 - 8: uncovered whit n adjacent bombs
        9:     uncovered whit a bomb in it
        10:    covered with a flag
        11:    covered with a question mark
        12:    covered without anything"""
        
        # Exit immediately if new status is equal to current one
        if newStatus == self.status:
            return
        
        self.status = newStatus
        self[ 'image' ] = images[ self.status ]

                
    def GetStatus( self ):
        """Return the current cell display status."""
        return self.status
        
    def Reveal( self ):
        """Uncover the cell.
        
        Uncover the cell only if there is a bomb in it, or
        without any bomb, but with a flag (false positive)."""
                
        if self.ucell.HasMine():
            if self.status == CELL_STATUS_COVERED or \
               self.status == CELL_STATUS_FLAG or \
               self.status == CELL_STATUS_QMARK:
                # Reveael a bomb
                self._SetStatus( CELL_STATUS_BOMB )
            else:
                # Reveal a false negative (a bomb without flag)
                self._SetStatus( CELL_STATUS_FALSEN )
        elif self.status == CELL_STATUS_FLAG:
            # Reveal a false positive (a flag without bomb)
            self._SetStatus( CELL_STATUS_FALSEP )
            

          
        
#-------------------------------------------------------------------------------
# A class to implement a minesweeper table as a matrix of CellButton istances
#-------------------------------------------------------------------------------
class MinesweeperTable( Frame ):
    """A class to implement a Minesweeper panel.
    
    Actually it is a matrix of CellButton instances. It is linked to a instance
    of minesweeper.Game: the real underlying game."""
    
    
    def __init__( self, master = None, game = None ):
        """Initialize an instance of game table.
        
        master: the Tk master widget
        game:   is an existing minesweeper.Game instance.
                If None __init__() create a random new one."""
        Frame.__init__( self, master )
        
        # Init the game
        if game:
            self.game = game
        else:
            # If there is no existing game, create a new one using currently
            # active option for table dimension & mines number
            self.game = minesweeper.Game(
                options[ option ][ 'nrows' ],
                options[ option ][ 'ncols' ],
                options[ option ][ 'nmines' ]
            )
        nrows = len( self.game )
        ncols = len( self.game[ 0 ] )
        self.create_cells()
        self.UpdateAllCells()
        
        # Create the status line
        self.statusMessage = StringVar()
        Label( self,
               textvariable = self.statusMessage,
               padding = ( 0, 3, 0, 3 )
             ).grid( row = nrows + 1, column = 0, columnspan = ncols + 1 )
        self.UpdateStatusMessage()
        
    def create_cells( self ):
        """Create all the cell widgets in the table."""

        nrows = len( self.game )
        ncols = len( self.game[ 0 ] ) 
        self.cells = []
        for i in range( nrows ):
            row = []
            for j in range( ncols ):
                cell = CellButton( self, self.game[ i ][ j ] )
                row.append( cell )
            self.cells.append( row )
            
            # Append a rightbord image to close the row
            Tkinter.Label( self,
                           bd = 0,
                           image = images[ CELL_STATUS_RBORD ]
                         ).grid( row = i, column = len( row ) )
            
        # Create the bottom border
        for j in range( ncols ):
            Tkinter.Label( self,
                           bd = 0,
                           image = images[ CELL_STATUS_BBORD ]
                         ).grid( row = nrows, column = j )
                         
        # Create the bottom right corner
        Tkinter.Label( self,
                       bd = 0,
                       image = images[ CELL_STATUS_CBORD ]
                     ).grid( row = nrows, column = ncols )
        
        # Bind all used events on the cell widgets wiht the handlers
        self.BindAllEvents()

        
            
    def OnB1Enter( self, event ):
        """The mouse enter the cell with button 1 pressed: press
        again the cell, if it was yet pressed."""
        cell = event.widget
        if cell.pressed == CellButton.LEAVED:
            cell[ 'image' ] = images[ CELL_STATUS_PRESSED ]
            cell.pressed = CellButton.PRESSED

    def OnB1Leave( self, event ):
        """The mouse leaves a cell with button 1 pressed: reset
        the original image and sign as LEAVED."""
        cell = event.widget
        if cell.pressed == CellButton.PRESSED:
            cell[ 'image' ] = images[ cell.GetStatus() ]
            cell.pressed = CellButton.LEAVED

    def OnButton1( self, event ):
        """The mouse button 1 has pressed in the cell: sign as PRESSED,
        but not if a flag is there."""
        cell = event.widget
        status = cell.GetStatus()
        assert cell.pressed == CellButton.UNPRESSED

        if status == CELL_STATUS_COVERED or status == CELL_STATUS_QMARK:
            cell[ 'image' ] = images[ CELL_STATUS_PRESSED ]
            cell.pressed = CellButton.PRESSED
                
    def OnButtonRelease1( self, event ):
        """The mouse button 1 has released on the cell: the cell
        has to be uncovered!"""
        cell = event.widget
        i, j = cell.ucell.GetCoordinates()
        
        if cell.pressed == CellButton.PRESSED:
            bomb = self.game.Uncover( i, j )
            
            if self.game[ i ][ j ].GetNeighborMinesNum() == 0:
                self.UpdateAllCells()
            else:
                event.widget.Update()
            
            if bomb:
                # If there is a bomd, you loose
                print _( "Bomb! Game over..." )
                self.EndLoosing()
            elif self.game.GetToDiscover() == 0:
                # If there's no more bombs to discover, you win
                print _( "You won!!!" )
                self.EndWinning()
            else:
                # Neither defeat nor victory: update the window's title
                self.master.RefreshTitle()

        cell.pressed = CellButton.UNPRESSED            

    def OnButton3( self, event ):
        """Handler for the mouse right click."""
        
        # Get coordinates of cell & current status
        status = event.widget.GetStatus()
        i, j = event.widget.ucell.GetCoordinates()
        
        if status == CELL_STATUS_COVERED:
            # Put a flag
            self.game.Flag( i, j )
            event.widget.Update()
            self.UpdateStatusMessage()
        elif status == CELL_STATUS_FLAG:
            # Remove flag and put a question mark
            self.game.QMark( i, j )
            event.widget.Update()
            self.UpdateStatusMessage()
        elif status == CELL_STATUS_QMARK:
            # Remove question mark (and put nothing)
            self.game.QMark( i, j, True )
            event.widget.Update()
            
        self.master.RefreshTitle()
            
    def UpdateAllCells( self ):
        """Update all cells on the table from the underlying minesweeper.Game instance."""
        for row in self.cells:
            for cell in row:
                cell.Update()
                
                
    def EndLoosing( self ):
        """Manage the defeat."""
        
        # Reveal all bombs
        for row in self.cells:
            for cell in row:
                cell.Reveal()
        
        self.UnbindAllEvents()
        self.game.SetModified( False )
        
        # Ask for Exit, Replay, Play a new game
        dialog = Dialog.Dialog(
            self,
            title = _( "You loosed!" ),
            icon = 'error',
            text = _( "You loosed...\nWhat do you want to do?" ),
            bitmap = 'warning',
            default = 0,
            strings = ( _( 'Exit' ),
                        _( 'Replay this game' ),
                        _( 'Play a new game' ) )
        )
        if dialog.num == 0:
            self.master.onQuit()
        elif dialog.num == 1:
            self.master.onReplayThisGame()
        else:
            self.master.onNewGame()
        
            
                
                
    def EndWinning( self ):
        """Manage the success!"""
        
        # Reveal all bombs
        for row in self.cells:
            for cell in row:
                cell.Reveal()
        
        # Unbind all cells
        self.UnbindAllEvents()
                        
        self.game.SetModified( False )
                
        # Ask for Exit, Play a new game
        dialog = Dialog.Dialog(
            self,
            title = _( "You Won!" ),
            icon = 'error',
            text = _( "You won...\nWhat do you want to do?" ),
            bitmap = 'info',
            default = 0,
            strings = ( _( 'Exit' ),
                        _( 'Play a new game' ) )
        )
        if dialog.num == 0:
            self.master.onQuit()
        else:
            self.master.onNewGame()
            
        
    def Restart( self ):
        """Restart the game with the same mines' set."""
        for row in self.cells:
            for cell in row:
                cell.destroy()
        self.game.Restart()
        self.create_cells()
        self.UpdateAllCells()
        self.UpdateStatusMessage()
        
    def UpdateStatusMessage( self ):
        """Ask the beyond game for data to update the status message."""
        remMines = self.game.nmines - self.game.nflags
        if remMines == 1:
            self.statusMessage.set( _( "1 remaining mine" ) )
        else:
            self.statusMessage.set( _( "%d remaining mines" ) % remMines )
            
    def IsModified( self ):
        """Return the modified flag status of underlying game."""
        return self.game.IsModified()
        
    def BindAllEvents( self ):
        """Bind all used events on the cells."""
        self.bind_class( CellButton.__name__, '<Button-1>', self.OnButton1 )
        self.bind_class( CellButton.__name__, '<B1-Leave>', self.OnB1Leave )
        self.bind_class( CellButton.__name__, '<B1-Enter>', self.OnB1Enter )
        self.bind_class( CellButton.__name__, '<ButtonRelease-1>', self.OnButtonRelease1 )
        self.bind_class( CellButton.__name__, '<Button-3>', self.OnButton3 )
        self.bind_class( CellButton.__name__, '<Control-Button-1>', self.OnButton3 )
        self.bind_class( CellButton.__name__, '<Button-2>', self.OnButton3 )

        
    def UnbindAllEvents( self ):
        """Unbind all used events from the cells."""
        self.unbind_class( CellButton.__name__, '<Button-1>' )
        self.unbind_class( CellButton.__name__, '<B1-Leave>' )
        self.unbind_class( CellButton.__name__, '<B1-Enter>' )
        self.unbind_class( CellButton.__name__, '<ButtonRelease-1>' )
        self.unbind_class( CellButton.__name__, '<Button-3>' )
        self.unbind_class( CellButton.__name__, '<Control-Button-1>' )
        self.unbind_class( CellButton.__name__, '<Button-2>' )

#-------------------------------------------------------------------------------
# My Options Window
#-------------------------------------------------------------------------------
class OptionWindow( Toplevel ):
    """A class for the options window."""
    
    def __init__( self, master = None ):
        """Initialize the option window with parent window."""
        Toplevel.__init__( self, master )
        
        self.title( _("Options") )
        
        # Use a frame to properly get the background color
        contents = Frame( self )
        contents[ 'padding' ] = 12
        
        # Set a label with instructions
        Label( contents,
            text = _("Choose table size and start a new game:"),
        ).grid( row = 0, column = 0, columnspan = 2, sticky = ( W, E ) ) 
        
        # Set three radio button to choose an option
        frame1 = Frame( contents, padding = ( 24, 24, 24, 48 ) )
        frame1.grid( row = 1, column = 0, sticky = N )
        self.choice = IntVar( self )
        self.choice.set( option )

        Radiobutton( frame1,
                     text = _('9 x 9, 10 mines'),
                     variable = self.choice,
                     value = 0,
                     command = self.OnChangeOption
                     ).grid( row = 1,
                             column = 0,
                             sticky = W )
        Radiobutton( frame1,
                     text = _('16 x 16, 40 mines'),
                     variable = self.choice,
                     value = 1,
                     command = self.OnChangeOption
                     ).grid(  row = 2, 
                              column = 0,
                              sticky = W )
        Radiobutton( frame1,
                     text = _('16 x 30, 99 mines'),
                     variable = self.choice,
                     value = 2,
                     command = self.OnChangeOption
                     ).grid( row = 3,
                             column = 0,
                             sticky = W )
                             
        # Widgets to set custom options
        frame2 = Frame( contents, padding = ( 24, 24, 24, 48 ) )
        frame2.grid( row = 1, column = 1, sticky = N )
        
        Radiobutton( frame2,
                     text = _('Custom'),
                     variable = self.choice,
                     value = 3,
                     command = self.OnChangeOption
                     ).grid( row = 0,
                             column = 1,
                             sticky = W )

        self.height = IntVar()
        self.height.set( options[ 3 ][ 'nrows' ] )
        self.labelHeight = Label( frame2, text = _('Height (9-24):'), padding = ( 24, 0, 0, 0 ) )
        self.labelHeight.grid( row = 1, column = 1, sticky = W )
        self.entryHeight = Entry( frame2, width = 4, textvariable = self.height,
            validate = 'focusout', validatecommand = self.ValidateHeight, invalidcommand = self.InvalidHeight )
        self.entryHeight.grid( row = 1, column = 2, sticky = W )
        
        self.width = IntVar()
        self.width.set( options[ 3 ][ 'ncols' ] )
        self.labelWidth = Label( frame2, text = _('Width (9-30):'), padding = ( 24, 0, 0, 0 ) )
        self.labelWidth.grid( row = 2, column = 1, sticky = W )
        self.entryWidth = Entry( frame2, width = 4, textvariable = self.width,
            validate = 'focusout', validatecommand = self.ValidateWidth, invalidcommand = self.InvalidWidth )
        self.entryWidth.grid( row = 2, column = 2, sticky = W )
        
        self.mines = IntVar()
        self.mines.set( options[ 3 ][ 'nmines' ] )
        self.labelMines = Label( frame2, text = _("Mines (10-668):"), padding = ( 24, 0, 0, 0 ) )
        self.labelMines.grid( row = 3, column = 1, sticky = W )
        self.entryMines = Entry( frame2, width = 4, textvariable = self.mines,
            validate = 'focusout', validatecommand = self.ValidateMines, invalidcommand = self.InvalidMines )
        self.entryMines.grid( row = 3, column = 2, sticky = W )
        
        self.RefreshCustomOptions()
        

        # Set the Ok & Cancel buttons
        Button( contents, text = 'Ok', command = self.onOk ).grid( row = 4, column = 0 )
        Button( contents, text = 'Cancel', command = self.onCancel ).grid( row = 4, column = 1 )
            
        # Put main frame on the screen
        contents.grid()
        
        # Grab the events from all the application
        self.grab_set()
        self.wm_transient( self.master )


    def onOk( self ):
        """Set new values for rows, columns and mines' number. Then close the
        options window."""
        global option, options
        
        option = self.choice.get()
        options[ 3 ][ 'nrows' ] = self.height.get()
        options[ 3 ][ 'ncols' ] = self.width.get()
        options[ 3 ][ 'nmines' ] = self.mines.get()
        self.master.persData.SaveOptions( option, options[ 3 ] )
        self.destroy()
        self.master.onNewGame()


    def onCancel( self ):
        """Close the options window without saving."""
        self.destroy()
        
    def RefreshCustomOptions( self ):
        """Refresh the enabled status of custom options widget."""
        state = ( "!" if self.choice.get() == 3 else "" ) + "disabled"
        self.labelHeight.state( ( state, ) )
        self.entryHeight.state( ( state, ) )
        self.labelWidth.state( ( state, ) )
        self.entryWidth.state( ( state, ) )
        self.labelMines.state( ( state, ) )
        self.entryMines.state( ( state, ) )
        
    def OnChangeOption( self ):
        """Handler of options radio buttons. It executes when the user check any
        of radio buttons."""
        self.RefreshCustomOptions()
        
    def ValidateHeight( self ):
        """Validate the height entry."""
        try:
            if self.height.get() < 9 or self.height.get() > 24:
                return False
            return True
        except ValueError:
            self.height.set( 0 )
            return False
        
    def ValidateWidth( self ):
        """Validate the width entry."""
        try:
            if self.width.get() < 9 or self.width.get() > 30:
                return False
            return True
        except ValueError:
            self.width.set( 0 )
            return False
        
    def ValidateMines( self ):
        """Validate the mines entry."""
        try:
            maxmines = self.width.get() * self.height.get()
            if self.mines.get() < 10 or self.mines.get() > min( maxmines, 668 ):
                return False
            return True
        except ValueError:
            self.mines.set( 0 )
            return False
        
    def InvalidHeight( self ):
        """Fix the invalid height value."""
        val = max( self.height.get(), 9 )
        val = min( val, 24 )
        self.height.set( val )

    def InvalidWidth( self ):
        """Fix the invalid width value."""
        val = max( self.width.get(), 9 )
        val = min( val, 30 )
        self.width.set( val )
        
    def InvalidMines( self ):
        """Fix the invalid mines value."""
        val = max( self.mines.get(), 10 )
        try:
            val = min( val, self.height.get() * self.width.get() )
        except ValueError:
            val = 10
        val = min( val, 668 )
        self.mines.set( val )

#-------------------------------------------------------------------------------
# My Help dialog
#-------------------------------------------------------------------------------
class HelpDialog( Toplevel ):
    """This is the Help dialog class widget. It show some help on the game."""
    
    def __init__( self, master = None ):
        """Initialize and assemble the Help window."""
        Toplevel.__init__( self, master )
        
        self.title( _( "%s Help" ) % APP_NAME )
        
        # Create a Frame widget
        frame = Frame( self )
        frame[ "padding" ] = 12
        
        # Put a simple text on the screen
        Label( frame, text = _("Hello, this is a very simple minesweeper game.\n\n"
            "The game rules are simple:\n"
            "1) you have to discover all cells without mine to win;\n"
            "2) if you discover a cell with a mine, you loose.\n\n"
            "To discover a cell, click on it with the mouse.\n\n"
            "In order to simplify your task, every cell you discover\n"
            "indicates the number of mines in the adjacent cells.\n\n"
            "You can also mark cells with a flag or a question mark (?)\n"
            "to remember your hypothesis: every time you right\n"
            "click (or Control+click) on an covered cell you cycle between\n"
            "'unmarked' --> 'flagged' --> 'question mark' stati.\n\n"
            "Explore the File menu to find some useful command!\n\n"
            "Enjoy!") ).grid( row = 0, column = 0 )
        
        
        # Put a close button
        Button( frame, text = _('Close'), command = self.destroy ).grid(
            row = 10, column = 0, sticky = E )
        
        
        # Put the frame on the screen
        frame.grid()


#-------------------------------------------------------------------------------
# My Toplevel Window Class
#-------------------------------------------------------------------------------
class RootWindow( Tk ):
    """A class for the toplevel window of the application."""
    
    def __init__( self ):
        """Init my toplevel window."""
        Tk.__init__( self )
        
        # Create the images lists
        for name in imagesFilenames:
            img = PhotoImage()
            img[ 'file' ] = name
            images.append( img )

        # Create the menus
        self.menubar = Menu( self )
        self[ 'menu' ] = self.menubar
        
        # Menu File
        self.menu_file = Menu( self.menubar )
        self.menubar.add_cascade( menu = self.menu_file, label = _( 'File' ) )
        self.menu_file.add_command( label = _( 'New game' ), command = self.onNewGame )
        self.menu_file.add_command( label = _( 'Replay this game' ),
            command = self.onReplayThisGame )
        self.menu_file.add_command( label = _( 'Load' ), command = self.OnLoad )
        self.menu_file.entryconfigure( self.menu_file.index( _( 'Load' ) ), state = 'disabled' )
        self.menu_file.add_command( label = _( 'Save' ), command = self.OnSave )
        self.menu_file.add_command( label = _( 'Options...' ), command = self.onOptions )
        self.menu_file.add_separator()
        self.menu_file.add_command( label = _( 'Quit' ), command = self.onQuit )
        
        # Load options from save file. If there is a valid game in the file,
        # enable File->Load command
        self.persData = PersistentData( SAVE_FILE_NAME )
        global option, options
        try:
            game = self.persData.LoadGame()
            if type( game ) == minesweeper.Game:
                self.menu_file.entryconfigure( self.menu_file.index( _( 'Load' ) ), state = 'normal' )
            option, options[ 3 ] = self.persData.LoadOptions()
        except IOError:
            pass
            
        
        # Menu Help
        self.menu_help = Menu( self.menubar )
        self.menubar.add_cascade( label = _( 'Help' ), menu = self.menu_help )
        self.menu_help.add_command( label = _( "%s Help..." ) % APP_NAME, command = self.OnHelp )
        self.menu_help.add_command( label = _( 'About %s' ) % APP_NAME + '...', command = self.OnAbout )
        
        # Intercept close command from Wm
        self.wm_protocol( "WM_DELETE_WINDOW", self.onQuit )
		
		# Intercept Command+Q on Macintosh
        if self.tk.call( 'tk', 'windowingsystem' ) == "aqua":
            self.createcommand( "exit", self.onQuit )
        
        # Create a new game
        self.onNewGame()


    def onNewGame( self ):
        """Handler of File->New game command."""
        if hasattr( self, 'table' ):
            self.table.destroy()

        self.table = MinesweeperTable( self )
        self.table.grid()
        self.RefreshTitle()

    def onReplayThisGame( self ):
        """Handler of File->Replay this game command."""
        self.table.Restart()
        self.RefreshTitle()

    def onOptions( self ):
        """Handler of File->Options... command."""
        OptionWindow( self )

    def onQuit( self ):
        """Handler of File->Quit command."""
        confirm = False
        
        # Ask for user confirmation if the game is modified
        if not self.table.IsModified():
            confirm = True
        else:
            import tkMessageBox
            confirm = tkMessageBox.askyesno( title = "Quit",
                                             message = "Are you shure you want to quit?" )
        
        if confirm:
            self.destroy()
            
    def OnSave( self ):
        """Save current game on ~/.minesweeptk_save."""
        self.persData.SaveGame( self.table.game )
        self.table.game.SetModified( False )
        self.menu_file.entryconfigure( self.menu_file.index( _( 'Load' ) ), state = 'normal' )
        self.RefreshTitle()

    def OnLoad( self ):
        """Load game from ~/.minesweeptk_save."""
        game = self.persData.LoadGame()
        self.table.destroy()
        self.table = MinesweeperTable( self, game )
        self.table.game.SetModified( False )
        self.table.grid()
        self.RefreshTitle()
                
    def OnAbout( self ):
        """Visualize an About dialog and exit."""
        import tkMessageBox
        tkMessageBox.showinfo(
            title = "About " + APP_NAME,
            message = APP_NAME + " v" + minesweeper.VERSION + """
            
A minesweeper game in Python and Tk
written by Alessandro Morgantini <gpz500@technologist.com>
Homepage: http://www.morgantini.org/

Copyright (C) 2012 Alessandro Morgantini
Released under the terms of GPLv3
(http://www.gnu.org/licenses/gpl.html)"""
        )
        
    def OnHelp( self ):
        """Handler of Help->Minesweeptk Help command.
        Open an simple help dialog and exit."""
        HelpDialog( self )
        
        
    def RefreshTitle( self ):
        """Refresh the title string in base of the underlying game table."""
        try:
            modSign = "*" if self.table.IsModified() else ""
        except AttributeError:
            modSign = ""
            
        newTitle = modSign + APP_NAME
        if self.title() != newTitle:
            self.title( newTitle )
        

if __name__ == '__main__':
    """It means that the module is opened as an application."""                    
    root = RootWindow()

    # Put off the tearoff menus
    root.option_add( '*tearOff', False )
    
    # Set non resizable
    root.wm_resizable( False, False )
    
    # Start the game
    root.mainloop()

