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
        push = self.status <= 9 
                
    def GetStatus( self ):
        """Return the current status."""
        return self.status
        
    def Reveal( self ):
        """Update the status of the button in base of corresponding cell."""
                
        if self.cell.HasMine():
            self._SetStatus( 9 )
            
        

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
            
        else:
            event.widget.Update()
        
        
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
        else:
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
                # cell[ 'state' ] = 'disabled'
                cell.unbind('<ButtonRelease-1>')
                cell.unbind('<Button-3>')
                
                
    def EndWinning( self ):
        """Exit with success!"""
        
        for row in self.cells:
            for cell in row:
                cell.unbind('<ButtonRelease-1>')
                cell.unbind('<Button-3>')
                
        
                    
    
root = Tkinter.Tk()

# Load images' files
for name in imagesFilenames:
    img = Tkinter.PhotoImage()
    img[ 'file' ] = name
    images.append( img )
    
# Insert File menu
fileMenu = Tkinter.Menubutton()
fileMenu[ 'text' ] = 'File'
fileMenu.pack()
    
table = MinesweeperTable( master = root, nrows = 16, ncols = 30, nmines = 99 )
table.pack()
root.mainloop()

