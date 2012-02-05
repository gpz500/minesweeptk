"""This program implements a personal version of Windows minesweeper game.

It uses the module minesweeper.py which gives two classes:
- Cell, for a single cell
- Game, which is a matrix of Cells."""

import sys                  # To exit from the interpreter
import Tkinter              # For GUI stuff
from Tkinter import *       
from ttk import *
import minesweeper          # For the minesweeper game

# The global list of Tkinter.Image objects to implement
# overimpression statuses on the button

# Define constants for all cell statuses

CELL_STATUS_ZERO, CELL_STATUS_ONE, CELL_STATUS_TWO, CELL_STATUS_THREE, \
CELL_STATUS_FOUR, CELL_STATUS_FIVE, CELL_STATUS_SIX, CELL_STATUS_SEVEN, \
CELL_STATUS_EIGHT, CELL_STATUS_BOMB, CELL_STATUS_FLAG, CELL_STATUS_QMARK, \
CELL_STATUS_COVERED, CELL_STATUS_PRESSED = range( 14 )

imagesFilenames = ( 'zero.gif', 'one.gif', 'two.gif', 'three.gif',
                    'four.gif', 'five.gif', 'six.gif', 'seven.gif',
                    'eight.gif', 'bomb.gif', 'flag.gif', 'q_mark.gif',
                    'covered.gif', 'pressed.gif' )
images = []

# Size of table and number of mines
option = 1
options = ( { "nrows": 9, "ncols": 9, "nmines": 10 },
            { "nrows": 16, "ncols": 16, "nmines": 40 },
            { "nrows": 16, "ncols": 30, "nmines": 99 } )

#-------------------------------------------------------------------------------
# A class to implement a single cell
#-------------------------------------------------------------------------------
class CellButton( Tkinter.Label ):
    """A class to implement a Minesweeper cell button."""
    
    UNPRESSED = 0   # Cell non-pressed
    PRESSED   = 1   # Cell pressed & mouse into
    LEAVED    = 2   # Cell pressed & mouse out
    
    def __init__( self, row, col, master = None ):
        """It define some cell attributes."""
        Tkinter.Label.__init__( self, master )
        
        self[ 'bd' ] = 0
        self.row = row
        self.col = col
        self.grid( row = row, column = col )
        self.status = -1
        self.cell = master.game[ row ][ col ]

        # A variable to manage the press status of the cell
        self.pressed = self.UNPRESSED 
        
    def Update( self ):
        """Update the status of the button in base of corresponding cell."""
        cellSt = self.cell.GetStatus()
        
        if cellSt == minesweeper.Cell.COVERED:
            newStatus = 12
        elif cellSt == minesweeper.Cell.FLAG:
            newStatus = 10
        elif cellSt == minesweeper.Cell.Q_MARK:
            newStatus = 11
        elif self.cell.HasMine():
            newStatus = 9
        else:
            newStatus = self.cell.GetNeighborMinesNum()
            
        self._SetStatus( newStatus )
        
        
    def _SetStatus( self, newStatus ):
        """Set the status of cell.
        
        Stati from 0 to 8 mean: pushed button whit n neighbor bombs
        9: bomb in it
        10: covered with flag
        11: covered with question mark
        12: covered without anything"""
        
        # Exit immediately if new status is equal to current one
        if newStatus == self.status:
            return
        
        self.status = newStatus
        self[ 'image' ] = images[ self.status ]

                
    def GetStatus( self ):
        """Return the current status."""
        return self.status
        
    def Reveal( self ):
        """Update the status of the button in base of corresponding cell."""
                
        if self.cell.HasMine():
            self._SetStatus( 9 )

    def UnbindAllEvents( self ):
        self.unbind( '<Button-1>' )
        self.unbind( '<B1-Leave>' )
        self.unbind( '<B1-Enter>' )
        self.unbind( '<ButtonRelease-1>' )
        self.unbind( '<Button-3>' )
        self.unbind( '<Control-Button-1>' )
        self.unbind( '<Control-ButtonRelease-1>' )
        
            
        
#-------------------------------------------------------------------------------
# A class to implement a minesweeper table as a matrix of CellButton istances
#-------------------------------------------------------------------------------
class MinesweeperTable( Frame ):
    """A class to implement a Minesweeper panel.
    
    Actually it is a matrix of CellButton instances."""
    
    
    def __init__( self, nrows = 16, ncols = 30, nmines = 99, master = None ):
        """Initialize an instance of game."""
        Frame.__init__( self, master )
        
        # Init the game
        self.game = minesweeper.Game( nrows, ncols, nmines )

        # Init cell buttons
        self.nrows = nrows
        self.ncols = ncols
        self.create_cells()
        self.UpdateAllCells()
        
        # Set some padding
        self[ 'padding' ] = 12
        
        
    def create_cells( self ):
        """Just a test function which create a lot of cells button."""

        self.cells = []
        for i in range( self.nrows ):
            row = []
            for j in range( self.ncols ):
                cell = CellButton( i, j, self )
                cell.bind( '<Button-1>', self.OnButton1 )
                cell.bind( '<B1-Leave>', self.OnB1Leave )
                cell.bind( '<B1-Enter>', self.OnB1Enter )
                cell.bind( '<ButtonRelease-1>', self.OnButtonRelease1 )
                cell.bind( '<Button-3>', self.OnButton3 )
                cell.bind( '<Control-Button-1>', self.OnButton3 )
                cell.bind( '<Control-ButtonRelease-1>', self.Hole )
                row.append( cell )
            self.cells.append( row )

    def OnB1Enter( self, event ):
        """Repress the cell if it was pressed."""
        cell = event.widget
        if cell.pressed == CellButton.LEAVED:
            cell[ 'image' ] = images[ CELL_STATUS_PRESSED ]
            cell.pressed = CellButton.PRESSED

    def OnB1Leave( self, event ):
        """Set original status."""
        cell = event.widget
        if cell.pressed == CellButton.PRESSED:
            cell[ 'image' ] = images[ cell.GetStatus() ]
            cell.pressed = CellButton.LEAVED

    def Hole( self, event ):
        """Hole handler. Intercept events and do nothing!"""
        pass

    def OnButton1( self, event ):
        """Handler of mouse left (primary) click."""
        cell = event.widget
        status = cell.GetStatus()
        assert cell.pressed == CellButton.UNPRESSED

        if status == CELL_STATUS_COVERED or status == CELL_STATUS_QMARK:
            cell[ 'image' ] = images[ CELL_STATUS_PRESSED ]
            cell.pressed = CellButton.PRESSED
                
    def OnButtonRelease1( self, event ):
        """Handler for the mouse click."""
        cell = event.widget
        i = event.widget.row
        j = event.widget.col
        
        if cell.pressed == CellButton.PRESSED:
            bomb = self.game.Uncover( i, j )
            
            if self.game[ i ][ j ].GetNeighborMinesNum() == 0:
                self.UpdateAllCells()
            else:
                event.widget.Update()
            
            if bomb:
                print "Bomb! Game over..."
                self.EndLoosing()
            # Check for victory
            elif self.game.GetToDiscover() == 0:
                print "You won!!!"
                self.EndWinning()

        cell.pressed = CellButton.UNPRESSED            

    def OnButton3( self, event ):
        """Handler for the mouse right click."""
        
        # Get coordinates of cell & current status
        status = event.widget.GetStatus()
        i = event.widget.row
        j = event.widget.col
        
        if status == CELL_STATUS_COVERED:
            self.game.Flag( i, j )
            event.widget.Update()
        elif status == CELL_STATUS_FLAG:
            self.game.QMark( i, j )
            event.widget.Update()
        elif status == CELL_STATUS_QMARK:
            self.game.QMark( i, j, True )
            event.widget.Update()
            
    def UpdateAllCells( self ):
        """Update all cells on the table."""
        for row in self.cells:
            for cell in row:
                cell.Update()
                
                
    def EndLoosing( self ):
        """Exit with error and block the game."""
        
        for row in self.cells:
            for cell in row:
                cell.Reveal()
                cell.UnbindAllEvents()
        
        import tkMessageBox
        choice = tkMessageBox.askyesnocancel(
            title = "You loosed!",
            icon = 'error',
            message = """You loosed. Press:
            Yes to quit
            No to replay same game
            Cancel to play a new game""" )
        if choice == 0:
            self.master.onReplayThisGame()
        elif choice == 1:
            sys.exit()
        else:
            self.master.onNewGame()
            
                
                
    def EndWinning( self ):
        """Exit with success!"""
        
        for row in self.cells:
            for cell in row:
                cell.UnbindAllEvents()
                
        import tkMessageBox
        choice = tkMessageBox.askyesno(
            title = "You won!",
            icon = 'info',
            message = """You won! Press
            Yes to quit
            No to play a new game""" )
        if choice == 0:
            self.master.onNewGame()
        else:
            sys.exit()
        
    def Restart( self ):
        """Restart the game with the same mines' set."""
        self.game.Restart()
        self.create_cells()
        self.UpdateAllCells()

#-------------------------------------------------------------------------------
# My Options Window
#-------------------------------------------------------------------------------
class OptionWindow( Toplevel ):
    """A class for the options window."""
    
    def __init__( self, master = None ):
        """Initialize the option window with parent window."""
        Toplevel.__init__( self, master )

        # Set a frame to get the background color
        frame = Frame( self )
        frame[ 'padding' ] = ( 3, 3, 12, 12 )
        
        # Set tree radio button to choose an option
        self.choice = IntVar( self )
        self.choice.set( option )

        Radiobutton( frame, text = '9 x 9, 10 mines',
            variable = self.choice, value = 0 ).grid( row = 0,
            column = 0,columnspan = 2, sticky = W )
        Radiobutton( frame, text = '16 x 16, 40 mines', variable = self.choice,
            value = 1 ).grid(  row = 1, column = 0, columnspan = 2,
            sticky = W )
        Radiobutton( frame, text = '16 x 30, 99 mines', variable = self.choice,
            value = 2 ).grid(  row = 2, column = 0, columnspan = 2,
            sticky = W )

        # Set the Ok & Cancel buttons
        Button( frame, text = 'Ok', command = self.onOk ).grid( row = 3,
            column = 0 )
        Button( frame, text = 'Cancel', command = self.onCancel ).grid( row = 3,
            column = 1 )
            
        # Put frame on the screen
        frame.grid()


    def onOk( self ):
        """Set new values for rows, columns and mines' number. Then close the
        options window."""
        global option
        option = self.choice.get()        
        self.destroy()
        self.master.onNewGame()


    def onCancel( self ):
        """Close the options window without saving."""
        self.destroy()






#-------------------------------------------------------------------------------
# My Toplevel Window Class
#-------------------------------------------------------------------------------
class RootWindow( Tk ):
    """A class for the toplevel window of my app."""
    
    def __init__( self, title = "" ):
        """Init my toplevel window."""
        Tk.__init__( self )

        # Create the images lists
        for name in imagesFilenames:
            img = PhotoImage()
            img[ 'file' ] = name
            images.append( img )

        # Set the window title
        self.title( title )

        # Create the menus
        self.menubar = Menu( self )
        self[ 'menu' ] = self.menubar
        self.menu_file = Menu( self.menubar )
        self.menubar.add_cascade( menu = self.menu_file, label = 'File' )
        self.menu_file.add_command( label = 'New game', command = self.onNewGame )
        self.menu_file.add_command( label = 'Replay this game',
            command = self.onReplayThisGame )
        self.menu_file.add_command( label = 'Options...', command = self.onOptions )
        self.menu_file.add_separator()
        self.menu_file.add_command( label = 'Quit', command = self.onQuit )

        # Create a new game
        self.onNewGame()


    def onNewGame( self ):
        """Handler of File->New game command."""
        if hasattr( self, 'table' ):
            self.table.destroy()

        self.table = MinesweeperTable( master = self, **options[ option ] )
        self.table.grid()

    def onReplayThisGame( self ):
        """Handler of File->Replay this game command."""
        self.table.Restart()

    def onOptions( self ):
        """Handler of File->Options... command."""
        options = OptionWindow( self )

    def onQuit( self ):
        """Handler of File->Quit command."""
        sys.exit()

if __name__ == '__main__':
    """It means that the module is opened as an application."""                    
    root = RootWindow( "Minesweeper" )

    # Put off the tearoff menus
    root.option_add( '*tearOff', FALSE )

    
    # Start the game
    root.mainloop()

