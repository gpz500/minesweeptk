"""This program implements a personal version of Windows minesweeper game.

It uses the module minesweeper.py which gives two classes:
- Cell, for a single cell
- Game, which is a matrix of Cells."""

import Tkinter      # For GUI stuff
import minesweeper  # For the minesweeper game

# The global list of Tkinter.Image objects to implement
# overimpression statuses on the button
imagesFilenames = ( 'zero.gif', 'one.gif', 'two.gif', 'three.gif',
                    'four.gif', 'five.gif', 'six.gif', 'seven.gif',
                    'eight.gif', 'bomb.gif', 'flag.gif', 'q_mark.gif',
                    'covered.gif' )
images = []

# Size of table and number of mines
option = 1
options = ( ( 9, 9, 10 ),
            ( 16, 16, 40 ),
            ( 16, 30, 99 ) )

#-------------------------------------------------------------------------------
# A class to implement a single cell
#-------------------------------------------------------------------------------
class CellButton( Tkinter.Label ):
    """A class to implement a Minesweeper cell button."""
    
    def __init__( self, row, col, master = None ):
        """It define some cell attributes."""
        Tkinter.Label.__init__( self, master )
        
        self[ 'bd' ] = 0
        self.row = row
        self.col = col
        self.grid( row = row, column = col )
        self.status = -1
        self.cell = master.game[ row ][ col ]
        
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
            
        
#-------------------------------------------------------------------------------
# A class to implement a minesweeper table as a matrix of CellButton istances
#-------------------------------------------------------------------------------
class MinesweeperTable( Tkinter.Frame ):
    """A class to implement a Minesweeper panel.
    
    Actually it is a matrix of CellButton instances."""
    
    
    def __init__( self, nrows = 16, ncols = 30, nmines = 99, master = None ):
        """Initialize an instance of game."""
        Tkinter.Frame.__init__( self, master )
        
        # Init the game
        self.game = minesweeper.Game( nrows, ncols, nmines )

        # Init cell buttons
        self.nrows = nrows
        self.ncols = ncols
        self.create_cells()
        self.UpdateAllCells()
        
        
    def create_cells( self ):
        """Just a test function which create a lot of cells button."""

        self.cells = []
        for i in range( self.nrows ):
            row = []
            for j in range( self.ncols ):
                cell = CellButton( i, j, self )
                cell.bind( '<ButtonRelease-1>', self.OnMouseRelease )
                cell.bind( '<Control-Button-1>', self.OnRightClick )
                cell.bind( '<Control-ButtonRelease-1>', self.Hole )
                cell.bind( '<Button-3>', self.OnRightClick )
                row.append( cell )
            self.cells.append( row )

    def Hole( self, event ):
        """Hole handler. Intercept events and do nothing!"""
        pass
                
    def OnMouseRelease( self, event ):
        """Handler for the mouse click."""
        status = event.widget.GetStatus()
        i = event.widget.row
        j = event.widget.col
        
        
        if status == 12 or status == 11:
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
            

    def OnRightClick( self, event ):
        """Handler for the mouse right click."""
        
        # Get coordinates of cell & current status
        status = event.widget.GetStatus()
        i = event.widget.row
        j = event.widget.col
        
        if status == 12:
            self.game.Flag( i, j )
            event.widget.Update()
        elif status == 10:
            self.game.QMark( i, j )
            event.widget.Update()
        elif status == 11:
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
                cell.unbind('<ButtonRelease-1>')
                cell.unbind('<Button-3>')
                
                
    def EndWinning( self ):
        """Exit with success!"""
        
        for row in self.cells:
            for cell in row:
                cell.unbind('<ButtonRelease-1>')
                cell.unbind('<Button-3>')
                
        
    def Restart( self ):
        """Restart the game with the same mines' set."""
        self.game.Restart()
        self.create_cells()
        self.UpdateAllCells()

#-------------------------------------------------------------------------------
# My Options Window
#-------------------------------------------------------------------------------
class OptionWindow( Tkinter.Toplevel ):
    """A class for the options window."""
    
    def __init__( self, master = None ):
        """Initialize the option window with parent window."""
        Tkinter.Toplevel.__init__( self, master )

        # Set tree radio button to choose an option
        self.choice = Tkinter.IntVar( self )
        self.choice.set( option )

        self.radio0 = Tkinter.Radiobutton( self, text = '9 x 9, 10 mines', variable = self.choice, value = 0 )
        self.radio1 = Tkinter.Radiobutton( self, text = '16 x 16, 40 mines', variable = self.choice, value = 1 )
        self.radio2 = Tkinter.Radiobutton( self, text = '16 x 30, 99 mines', variable = self.choice, value = 2 )

        self.radio0.pack()
        self.radio1.pack()
        self.radio2.pack()

        # Set the Ok & Cancel buttons
        self.ok_button = Tkinter.Button( self )
        self.cancel_button = Tkinter.Button( self )

        self.ok_button.config( text = 'Ok', command = self.onOk )
        self.cancel_button.config( text = 'Cancel', command = self.onCancel )

        self.ok_button.pack()
        self.cancel_button.pack()
        

    def onOk( self ):
        """Set new values for rows, columns and mines' number. Then close the options window."""
        global option
        option = self.choice.get()        
        self.destroy()


    def onCancel( self ):
        """Close the options window without saving."""
        self.destroy()






#-------------------------------------------------------------------------------
# My Toplevel Window Class
#-------------------------------------------------------------------------------
class RootWindow( Tkinter.Tk ):
    """A class for the toplevel window of my app."""
    
    def __init__( self ):
        """Init my toplevel window."""
        Tkinter.Tk.__init__( self )

        # Create the images lists
        for name in imagesFilenames:
            img = Tkinter.PhotoImage()
            img[ 'file' ] = name
            images.append( img )

        # Create the menus
        self.menubar = Tkinter.Menu( self )
        self[ 'menu' ] = self.menubar
        self.menu_file = Tkinter.Menu( self.menubar )
        self.menubar.add_cascade( menu = self.menu_file, label = 'File' )
        self.menu_file.add_command( label = 'New game', command = self.onNewGame )
        self.menu_file.add_command( label = 'Replay this game', command = self.onReplayThisGame )
        self.menu_file.add_command( label = 'Options...', command = self.onOptions )
        self.menu_file.add_separator()
        self.menu_file.add_command( label = 'Quit', command = self.onQuit )

        # Create a new game
        self.onNewGame()


    def onNewGame( self ):
        """Handler of File->New game command."""
        if hasattr( self, 'table' ):
            self.table.destroy()

        self.table = MinesweeperTable( master = self, nrows = options[ option ][ 0 ],
                                                      ncols = options[ option ][ 1 ],
                                                      nmines = options[ option ][ 2 ] )
        self.table.pack()

    def onReplayThisGame( self ):
        """Handler of File->Replay this game command."""
        self.table.Restart()

    def onOptions( self ):
        """Handler of File->Options... command."""
        options = OptionWindow( self )

    def onQuit( self ):
        """Handler of File->Quit command."""
        exit()

                    
root = RootWindow()

# Put off the tearoff menus
root.option_add( '*tearOff', Tkinter.FALSE )

    
# Start the game
root.mainloop()

