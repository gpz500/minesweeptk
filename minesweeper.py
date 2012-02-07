"""Minesweeper game.

This module implements two classes to implement a minesweeper game.
The classes are:
    - Cell, for a single cell
    - Game, for a two dimensional array of cells
    
If game = Game(), the cells are addressed as game[i][j] where 0 <= i <= nrows
and 0 <= j <= ncols.
"""


__author__ = "Alessandro Morgantini <gpz500@technologist.com>"
__version__ = "$Revision$"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2012 Alessandro Morgantini"
__license__ = "Python"


class MinesweeperError( Exception ):
    pass
    
class MinesweeperStatusError( MinesweeperError ):
    pass
    
class MinesweeperAutoUncoverError( MinesweeperError ):
    pass
    
class MinesweeperCellError( MinesweeperError ):
    pass

class MinesweeperMinesCount( MinesweeperError ):
    pass

class Cell:
    """This is a class for a single cell.
    
    Create an instance of this class for every cell in the map when a game is
    started."""
    
    # Some usesul constants
    COVERED = 0
    REVEALED = 1
    FLAG = 2
    Q_MARK = 3
    
    def __init__( self, x, y ):
        """The init method for a instance.
        The arguments are:
    
        x, y:     the coordinates of the cell
        mine:     is there a mine (True or False)?"""
        if x < 0 or y < 0:
            raise MinesweeperCellError( "Coordinates must be both >= 0" )
    
        self.x = x
        self.y = y
            
        # This is the cell status (initially COVERED)
        self.status = self.COVERED
        
        # This is the number of neighbor cells with a mine (initially 0)
        self.neighborMines = 0
        
        # This is the presence of a mine or not (initially false)
        self.mine = False
        
    def SetNeighbors( self, neighbors ):
        """Set the actual number of neighbors."""
        self.neighbors = neighbors
        
    def GetNeighborMinesNum( self ):
        """Return the actual number of neighbors."""
        return self.neighborMines
        
    def IncNeighbors( self ):
        """Increment the numbers of neighbors mines by 1."""
        self.neighborMines += 1
        
    def GetCoordinates( self ):
        """Return a tuple with two elements: (x, y)."""
        return ( self.x, self.y )
        
    def HasMine( self ):
        """Return if the cell has a mine or not."""
        return self.mine
        
    def SetMine( self, reset = False ):
        """Set mine as true."""
        self.mine = not reset
        
    def GetStatus( self ):
        """Return the current status of cell."""
        return self.status
        
    def SetStatus( self, newstatus ):
        """Set current status of the cell. Return the old status."""
        if newstatus == self.status:
            raise MinesweeperStatusError( "Error: can't reassign the same status" )
        if self.status == Cell.FLAG and newstatus == Cell.REVEALED:
            raise MinesweeperStatusError( "Error: can't do the transition FLAG -> REVEALED" )
        if self.status == Cell.REVEALED:
            raise MinesweeperStatusError( "Error: can't come back from REVEALED status" )
        oldstatus = self.status
        self.status = newstatus
        return oldstatus
        
class Game( list ):
    """A class for a whole minesweeper game."""
    
    def __init__( self, nrows = 16, ncols = 30, nmines = 99 ):
        """Initialize a game with nrows, ncols and nmines set randomnly on the table."""
        
        # Check for the acceptable mines number
        if nmines > nrows * ncols:
            raise MinesweeperMinesCount( "Too much mines!" )
        
        # I have to create nrows list ncols cells
        self.cells = []
        
        # The number of cells without bombs: every time you discover a cell this
        # count cuts
        self.toDiscover = nrows * ncols - nmines
        
        # Save the number of mines
        self.nmines = nmines
        
        # The number of flags on the game (initially 0)
        self.nflags = 0
        
        # Create all the cells
        self.CreateCells( nrows, ncols )
        
        # Now I have to put nmines randomly in the cells
        mines = []
        while len( mines ) < nmines:
            # Computes a random position for the mine. If it already exists, compute a new one
            i, j = self.GetRandomPos()
            while ( i, j ) in mines:
                i, j = self.GetRandomPos()
            mines.append( (i, j) )
            self[ i ][ j ].SetMine()
            
        
        # Now I have a list of mines. For every mine I need to
        # increment the number of neighbors in the neighbors cells
        for i, j in mines:
            for cell in self.GetNeighborsList( i, j ):
                cell.IncNeighbors()
        


    def __getitem__( self, index ):
        """Game is a subclass of list, so it returns the index-th rows when asked."""
        return self.cells[ index ]
        
    
    def __len__( self ):
        """Return the number of rows."""
        return len( self.cells )
        
    def __iter__( self ):
        """Return an iterator object specifically for 'for'."""
        return self.cells.__iter__()
        
    def GetNeighborsList( self, i, j = -1 ):
        """Compute a list of neighbors."""
        li = []
        if j == -1:
            # i is the cell object
            j = i.y
            i = i.x
                
        imin = max( i - 1, 0 )
        imax = min( i + 1, len( self ) - 1 )
        jmin = max( j - 1, 0 )
        jmax = min( j + 1, len( self[ 0 ] ) - 1 )
        for ii in range( imin, imax + 1 ):
            for jj in range( jmin, jmax + 1 ):
                if ( ii, jj ) != ( i, j ): li.append( self[ ii ][ jj ] ) 
                
        return li
        
    def Uncover( self, i, j ):
        """Uncover the cell (i, j). Return True if there is a mine, False otherwise."""
        cell = self[ i ][ j ]
        oldStatus = cell.SetStatus( Cell.REVEALED )
        if oldStatus == Cell.FLAG:
            self.nflags -= 1
        self.toDiscover -= 1
        if cell.HasMine():
            return True
            
        # Undiscover the neighbords also, but only if this cell have non close mines
        if not cell.GetNeighborMinesNum():
            self.AutomaticUncover( cell )
                
        return False
        
    def AutomaticUncover( self, cell ):
        """Uncover a chain of cells by neighboroad relation."""
        for myCell in self.GetAutoUncoverList( cell ):
            oldStatus = myCell.SetStatus( Cell.REVEALED )
            if oldStatus == Cell.FLAG:
                self.nflags -= 1
            self.toDiscover -= 1
            
    def GetAutoUncoverList( self, cell ):
        """Return the list of cells to uncover automatically, starting from the supplied cell."""
        if cell.GetNeighborMinesNum():
            raise MinesweeperAutoUncoverError( "Error: can't automatic uncovers cells with some close mine!" )
        
        myFiltFunction = lambda x: x.GetStatus() != Cell.REVEALED and x.GetStatus() != Cell.FLAG
        toUncover = filter( myFiltFunction, self.GetNeighborsList( cell ) )
        for nei in toUncover:
            if not nei.GetNeighborMinesNum():
                neiToUncover = filter( myFiltFunction, [ item for item in self.GetNeighborsList( nei ) if not item in toUncover ] )
                toUncover.extend( neiToUncover )
                
        return toUncover
        
            
        
    def Flag( self, i, j, reset = False ):
        """Set/Reset a flag."""
        newStatus = Cell.COVERED if reset else Cell.FLAG
        oldStatus = self[ i ][ j ].SetStatus( newStatus )
        
        # Update the count of flags
        if oldStatus == Cell.FLAG and newStatus != Cell.FLAG:
            self.nflags -= 1
        elif oldStatus != Cell.FLAG and newStatus == Cell.FLAG:
            self.nflags += 1
        
    def QMark( self, i, j, reset = False ):
        """Set/Reset a question mark."""
        newstatus = Cell.COVERED if reset else Cell.Q_MARK
        oldstatus = self[ i ][ j ].SetStatus( newstatus )
        if oldstatus == Cell.FLAG:
            self.nflags -= 1
        
        
    def GetToDiscover( self ):
        """Return the number of cells remaining to discover."""
        return self.toDiscover
        
    def SetMines( self, minesList ):
        """Set a known minelist. minesList is a list of coordinates."""
        for row in self:
            for cell in row:
                cell.SetMine( not cell.GetCoordinates() in minesList )
                # Reset the number of neighbors
                cell.SetNeighbors( 0 )
                
        # I have a list of mines. For every mine I need to
        # increment the number of neighbors in the neighbors cells
        for i, j in minesList:
            for cell in self.GetNeighborsList( i, j ):
                cell.IncNeighbors()
                
    def GetMines( self ):
        """Return a list of coordinates of current mines."""
        mines = []
        for row in self:
            for cell in row:
                if cell.HasMine():
                    mines.append( cell.GetCoordinates() )            
        return mines
        
    def Restart( self ):
        """Reinit the game with the same mine list."""
        mines = self.GetMines()
        nrows = len( self )
        ncols = len( self[ 0 ] )
        
        # Recreate the cells matrix
        self.CreateCells( nrows, ncols )
        
        # Reset mines & counter
        self.SetMines( mines )
        self.toDiscover = nrows * ncols - len( mines )
        self.nflags = 0
        
        
    def CreateCells( self, nrows, ncols ):
        """(Re)create the cells matrix, erasing the possible exiting one."""
        
        self.cells = []
        for i in range( nrows ):
            row = []
            for j in range( ncols ):
                row.append( Cell( i, j ) )
                
            self.cells.append( row )

    def GetRandomPos( self ):
        """Static method to compute random pos between 0 - (nrows-1) and 0 - (ncols-1)."""
        import random
        i = random.randint( 0, len( self ) - 1 )
        j = random.randint( 0, len( self[ 0 ] ) - 1 )
        return ( i, j )
        
    def GetFlagsNum( self ):
        """Return the number of currently number of flags."""
        return self.nflags
        
    def GetMinesNum( self ):
        """Return the number of mines in the game."""
        return self.nmines

    
            
    
def PrintGame( game, unveil = False ):
    """Print the table of games, with actual covered, flagged, q_mark."""
    nrows = len( game )
    ncols = len( game[ 0 ] )
    lines = []
    
    # First & second line
    tents = [ ' ' ]     # First column for the ABC...
    units = [ ' ' ]
    for j in range( 1, ncols + 1 ):
        quot = j / 10
        remain = j % 10
        if quot:
            tents.append( str( quot ) )
        else:
            tents.append( ' ' )
        units.append( str( remain ) )
    lines.append( "".join( tents ) )
    lines.append( "".join( units ) )
    
    # The table
    for i in range( nrows ):
        line = [ chr( ord('A') + i ) ]
        for j in range( ncols ):
            status = game[ i ][ j ].GetStatus()
            neigh = game[ i ][ j ].GetNeighborMinesNum()
            
            if unveil:
                if game[ i ][ j ].HasMine():    line.append( '*' )
                # From here in on the cell does not have a mine
                elif status == Cell.FLAG:       line.append( 'E' )  # Error
                elif status == Cell.Q_MARK:     line.append( '?' )
                elif status == Cell.COVERED:    line.append( '-' )
                else:
                    # Uncovered
                    if neigh == 0:              line.append( ' ' )
                    else:                       line.append( str( neigh ) )
            else:
                if status == Cell.FLAG:         line.append( '*' )
                elif status == Cell.Q_MARK:     line.append( '?' )
                elif status == Cell.COVERED:    line.append( '-' )
                else:
                    # Uncovered
                    if neigh == 0:              line.append( ' ' )
                    else:                       line.append( str( neigh ) )
        
        
        lines.append( "".join( line ) )
    


    print "\n".join( lines )
            
        
    
    
if __name__ == '__main__':
    # Do a game on terminal
    import sys
    import readline
    import re
    myGame = Game( 9, 9, 10 )
    
    while True:
        PrintGame( myGame )
        command = raw_input( "[Q|B i j|? i j|R i j] > " )
        
        myResult = re.search( '^\s*[qQ]\s*$', command )
        if myResult:
            # Q: quit
            exit()
            
        myResult = re.search( '^\s*([bB\?rR])\s+([A-Za-z])\s+(\d+)\s*$', command )
        if myResult:
            command = myResult.group( 1 ).upper()
            i = ord( myResult.group( 2 ).upper() ) - ord( 'A' )
            j = int( myResult.group( 3 ) ) - 1
            
            try:
                if command == 'B':
                    # Sign a bomb
                    if myGame[ i ][ j ].GetStatus() == Cell.FLAG:
                        myGame.Flag( i, j, True )
                    else:
                        myGame.Flag( i, j )
                elif command == '?':
                    # Question mark on a cell
                    if myGame[ i ][ j ].GetStatus() == Cell.Q_MARK:
                        myGame.QMark( i, j, True )
                    else:
                        myGame.QMark( i, j )
                elif command == 'R':
                    # Reveal a cell
                    try:
                        mine = myGame.Uncover( i, j )
                    except MinesweeperStatusError:
                        mine = False
                    if mine:
                        print "Bomb!"
                        PrintGame( myGame, True )
                        command = raw_input( "Do you want to replay? [y|N]> " )
                        if not command or command.lstrip().upper()[ 0 ] != 'Y':
                            print "Bye!"
                            exit()
                        else:
                            myGame.Restart()
                    elif myGame.GetToDiscover() == 0:
                        print "You won!"
                        PrintGame( myGame )
                        exit()

            except IndexError:
                print "Position out of range!"

            except MinesweeperStatusError:
		pass

            
