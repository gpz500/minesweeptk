"""Unit test for module minesweeper.py.

minesweeper define two classes: Cell for a single cell and Game for a whole table.
"""

__author__ = "Alessandro Morgantini <gpz500@technologist.com>"
__version__ = "$Revision$"
__date__ = "$Date$"
__copyright__ = "Copyright © 2012-2023 Alessandro Morgantini"
__license__ = "GPLv2"

import unittest
import minesweeper

knownCoordinates = ( ( 0, 25 ),
                     ( 34, 5 ),
                     ( 12, 99 ),
                     ( 1, 3 ),
                     ( 3, 1 ),
                     ( 13, 10 ),
                     ( 0, 0 ),
                     ( 4, 4 ) )


class CellTest( unittest.TestCase ):
    
    statuses = ( minesweeper.Cell.COVERED,
                 minesweeper.Cell.FLAG,
                 minesweeper.Cell.Q_MARK,
                 minesweeper.Cell.REVEALED )

    def testSetStatus( self ):
        """Cell instances have to set properly its status."""
        cell = minesweeper.Cell( 10, 11 )
        cell.SetStatus( -1 )
        for status in self.statuses:
            cell.SetStatus( status )
            self.assertEqual( status, cell.GetStatus() )
            
    def testRetainCoordinates( self ):
        """Cell instances have to retain correctly their coordinates."""
        for x, y in knownCoordinates:
            cell = minesweeper.Cell( x, y )
            self.assertEqual( (x, y), cell.GetCoordinates() )
            
    def testCoordinatesNotNegative( self ):
        """Cell.__init__ must raise an exception when a coordinate is negative."""
        self.assertRaises( minesweeper.MinesweeperCellError, minesweeper.Cell, -1, 1 )
        self.assertRaises( minesweeper.MinesweeperCellError, minesweeper.Cell, 1, -1 )
        
    def testInvalidSetStatus( self ):
        """Cell instances have to raise exception in invalid status transition."""
        cell = minesweeper.Cell( 0, 0 )
        cell.SetStatus( minesweeper.Cell.REVEALED )
        self.assertRaises( minesweeper.MinesweeperStatusError, cell.SetStatus, minesweeper.Cell.COVERED )
        self.assertRaises( minesweeper.MinesweeperStatusError, cell.SetStatus, minesweeper.Cell.REVEALED )
        self.assertRaises( minesweeper.MinesweeperStatusError, cell.SetStatus, minesweeper.Cell.FLAG )
        self.assertRaises( minesweeper.MinesweeperStatusError, cell.SetStatus, minesweeper.Cell.Q_MARK )
        cell = minesweeper.Cell( 0, 0 )
        cell.SetStatus( minesweeper.Cell.FLAG )
        self.assertRaises( minesweeper.MinesweeperStatusError, cell.SetStatus, minesweeper.Cell.REVEALED )
        self.assertRaises( minesweeper.MinesweeperStatusError, cell.SetStatus, minesweeper.Cell.FLAG )
        cell = minesweeper.Cell( 0, 0 )
        cell.SetStatus( minesweeper.Cell.Q_MARK )
        self.assertRaises( minesweeper.MinesweeperStatusError, cell.SetStatus, minesweeper.Cell.Q_MARK )
        cell.SetStatus( minesweeper.Cell.REVEALED )
        self.assertRaises( minesweeper.MinesweeperStatusError, cell.SetStatus, minesweeper.Cell.REVEALED )
        
    def testIncNeighbors( self ):
        """Cell must properly increment the number o neighbors."""
        cell = minesweeper.Cell( 0, 0 )
        for n in range( 100 ):
            cell.SetNeighbors( n )
            cell.IncNeighbors()
            self.assertEqual( n + 1, cell.GetNeighborMinesNum() )
            
    def testMines( self ):
        """Cell must set & get mines properly."""
        cell = minesweeper.Cell( 0, 0 )
        self.assertEqual( False, cell.HasMine() )
        cell.SetMine()
        self.assertEqual( True, cell.HasMine() )
        cell.SetMine( reset = True )
        self.assertEqual( False, cell.HasMine() )
        
class GameTest( unittest.TestCase ):

    knownNeighboards = {
        ( 0, 0 ):   ( (0, 1), (1, 0), (1, 1) ),
        ( 15, 29 ): ( (14, 28), (14, 29), (15, 28) ),
        ( 0, 29 ):  ( (0, 28), (1, 28), (1, 29) ),
        ( 15, 0 ):  ( (14, 0), (14, 1), (15, 1) ),
        ( 0, 10 ):  ( (0, 9), (0, 11), (1, 9), (1, 10), (1, 11) ),
        ( 10, 0 ):  ( (9, 0), (9, 1), (10, 1), (11, 0), (11, 1) ),
        ( 10, 29 ): ( (9, 28), (9, 29), (10, 28), (11, 28), (11, 29) ),
        ( 15, 10 ): ( (14, 9), (14, 10), (14, 11), (15, 9), (15, 11) ),
        ( 3, 4 ):   ( (2, 3), (2, 4), (2, 5), (3, 3), (3, 5), (4, 3), (4, 4), (4, 5) )
    }
                         
    knownMines = ( (0, 1), (2, 1), (6, 3), (8, 5), (1, 1), (8, 3), (5, 1), (6, 6), (7, 8), (0, 7) )
    knownNeighMines = {
         ( 0, 0 ): 2,
         ( 0, 2 ): 2,
         ( 0, 6 ): 1,
         ( 0, 8 ): 1,
         ( 1, 0 ): 3,
         ( 1, 2 ): 3,
         ( 1, 6 ): 1,
         ( 1, 7 ): 1,
         ( 1, 8 ): 1,
         ( 2, 0 ): 2,
         ( 2, 2 ): 2,
         ( 3, 0 ): 1,
         ( 3, 1 ): 1,
         ( 3, 2 ): 1,
         ( 4, 0 ): 1,
         ( 4, 1 ): 1,
         ( 4, 2 ): 1,
         ( 5, 0 ): 1,
         ( 5, 2 ): 2,
         ( 5, 3 ): 1,
         ( 5, 4 ): 1,
         ( 5, 5 ): 1,
         ( 5, 6 ): 1,
         ( 5, 7 ): 1,
         ( 6, 0 ): 1,
         ( 6, 1 ): 1,
         ( 6, 2 ): 2,
         ( 6, 3 ): 1,
         ( 6, 4 ): 1,
         ( 6, 5 ): 1,
         ( 6, 7 ): 2,
         ( 6, 8 ): 1,
         ( 7, 2 ): 2,
         ( 7, 3 ): 2,
         ( 7, 4 ): 3,
         ( 7, 5 ): 2,
         ( 7, 6 ): 2,
         ( 7, 7 ): 2,
         ( 8, 2 ): 1,
         ( 8, 4 ): 2,
         ( 8, 6 ): 1,
         ( 8, 7 ): 1,
         ( 8, 8 ): 1
         }
    
    # Know autouncover for (8, 0)
    autoUncoverStart = ( 8, 0 )
    knownAutouncover = (
        ( 7, 0 ),
        ( 7, 1 ),
        ( 8, 1 ),
        ( 6, 0 ),
        ( 6, 1 ),
        ( 6, 2 ),
        ( 7, 2 ),
        ( 8, 2 )
    )

    def testInit( self ):
        """Game.__init__ must create the exact number of cells."""
        game = minesweeper.Game( 9, 21, 0 )
        self.assertEqual( 9, len( game ) )
        self.assertEqual( 21, len( game[ 0 ] ) )

    
    def testNeighbors( self ):
        """Game must compute the list of neighbors properly for a list of known cells."""
        game = minesweeper.Game()
        for ( i, j ), known in self.knownNeighboards.items():
            computedList = [ cell.GetCoordinates() for cell in game.GetNeighborsList( i, j ) ]
            self.assertEqual( known,  tuple( computedList ) )
            
    def testSetMines( self ):
        """Game must set correctly the mine from a known list."""
        if len( self.knownMines ) <= 25:
            nrows = 9
            ncols = 9
        elif 26 <= len( self.knownMines ) <= 76:
            nrows = 16
            ncols = 16
        else:
            nrows = 16
            ncols = 30
        game = minesweeper.Game( nrows, ncols, 0 )
        
        game.SetMines( self.knownMines )
        minesCount = 0
        for row in game:
            for cell in row:
                if cell.HasMine():
                    minesCount += 1
                    self.assertEqual( True, cell.GetCoordinates() in self.knownMines )
                else:
                    self.assertEqual( False, cell.GetCoordinates() in self.knownMines )
                    
        self.assertEqual( minesCount, len( self.knownMines ) )
                    
    def testNeighMines( self ):
        """Game must compute correctly the number of neighbors mines."""
        if len( self.knownMines ) <= 25:
            game = minesweeper.Game( 9, 9, 0 )
        elif 26 <= len( self.knownMines ) <= 76:
            game = minesweeper.Game( 16, 16, 0 )
        else:
            game = minesweeper.Game()
            
        game.SetMines( self.knownMines )
        for row in game:
            for cell in row:
                if not cell.HasMine():
                    if cell.GetCoordinates() in self.knownNeighMines.keys():
                        self.assertEqual( self.knownNeighMines[ cell.GetCoordinates() ], cell.GetNeighborMinesNum(),
                            "Should be %d, is %d (cell (%d, %d))" %
                                ( self.knownNeighMines[ cell.GetCoordinates() ],
                                  cell.GetNeighborMinesNum(),
                                  cell.GetCoordinates()[ 0 ],
                                  cell.GetCoordinates()[ 1 ] ) )
                    else:
                        self.assertEqual( 0, cell.GetNeighborMinesNum(),
                            "Should be 0, is %d (cell (%d, %d))" %
                                ( cell.GetNeighborMinesNum(),
                                  cell.GetCoordinates()[ 0 ],
                                  cell.GetCoordinates()[ 1 ] ) )
                
                         
    def testAutoUncover( self ):
        """Game must to autoreveal cells for known conditions."""
        if len( self.knownMines ) <= 25:
            game = minesweeper.Game( 9, 9, 0 )
        elif 26 <= len( self.knownMines ) <= 76:
            game = minesweeper.Game( 16, 16, 0 )
        else:
            game = minesweeper.Game()
            
        game.SetMines( self.knownMines )
        startCell = game[ self.autoUncoverStart[ 0 ] ][ self.autoUncoverStart[ 1 ] ]
        startCell.SetStatus( minesweeper.Cell.REVEALED )
        coordList = [ cell.GetCoordinates() for cell in game.GetAutoUncoverList( startCell ) ]
        self.assertEqual( tuple( coordList ), self.knownAutouncover )
        
    def testRestart( self ):
        """Game have to put all the cell statuses in COVERED and reset the count of uncovered cells."""
        game = minesweeper.Game()
        minesList = game.GetMines()
        
        game.QMark( 10, 21 )
        game.Flag( 10, 22 )
        game.QMark( 10, 20 )
        game.Flag( 10, 23 )
        
        
        game.Restart()
        for row in game:
            for cell in row:
                self.assertEqual( minesweeper.Cell.COVERED, cell.GetStatus() )
                
        self.assertEqual( game.GetMines(), minesList )
        self.assertEqual( len( game ) * len( game[ 0 ] ) - len( minesList ), game.GetToDiscover() )

    def testUncoverMine( self ):
        """Game.Uncover() must return True when hit a mine."""
        game = minesweeper.Game()
        minesList = game.GetMines()
        self.assertEqual( True, game.Uncover( minesList[ 0 ][ 0 ], minesList[ 0 ][ 1 ] ) )

    def testOutOfRangeIndexs( self ):
        """Game must raise IndexError exception when access inexistant cells."""
        game = minesweeper.Game()
        self.assertRaises( IndexError, lambda x: x[ 100 ][ 10 ], game )
        self.assertRaises( IndexError, lambda x: x[ 10 ][ 100 ], game )

    def testUnveils( self ):
        """Game must rasie no execption when uncover cells."""
        if len( self.knownMines ) <= 25:
            nrows = 9
            ncols = 9
        elif 26 <= len( self.knownMines ) <= 76:
            nrows = 16
            ncols = 16
        else:
            nrows = 16
            ncols = 30
        game = minesweeper.Game( nrows, ncols, 0 )
        
        game.SetMines( self.knownMines )
        game.Uncover( 8, 3 )
        game.Uncover( 4, 0 )
        game.Uncover( 2, 4 )
        
    def testModifiedStart( self ):
        """Game have start with False modified flag."""
        game = minesweeper.Game()
        self.assertEqual( False, game.IsModified() )
        
    def testModifiedSetUncover( self ):
        """Modified flag has to set automatically when uncover a cell."""
        game = minesweeper.Game()
        game.Uncover( 4, 6 )
        self.assertEqual( True, game.IsModified() )
        
    def testModifiedSetFlag( self ):
        """Modified flag has to set automatically when flag a cell."""
        game = minesweeper.Game()
        game.Flag( 4, 6 )
        self.assertEqual( True, game.IsModified() )
        
    def testModifiedSetQmark( self ):
        """Modified flag has to set automatically when q_mark a cell."""
        game = minesweeper.Game()
        game.QMark( 4, 6 )
        self.assertEqual( True, game.IsModified() )
        
    def testModifiedSetUnset( self ):
        """Modified has to work well explicitly."""
        game = minesweeper.Game()
        game.SetModified()
        self.assertEqual( True, game.IsModified() )
        game.SetModified( False )
        self.assertEqual( False, game.IsModified() )
        
    def testModifiedRestart( self ):
        """Modified has to return False when the game is restarted."""
        game = minesweeper.Game()
        game.SetModified()
        game.Restart()
        self.assertEqual( False, game.IsModified() )

        
if __name__ == '__main__':
    unittest.main()
    
