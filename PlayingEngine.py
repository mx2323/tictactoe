from abc import ABCMeta, abstractmethod, abstractproperty

#an enum for the position types on the board
class PositionType:
    BLANK="_"
    X="X"
    O="O"

class Board:
    #defines a position on the board
    class Position:
        def __init__(self, row, column):
            self.row = row
            self.column = column
    #defines a move: a position + a player   
    class Move:
        def __init__(self, Position, positionType):
            self.position = Position
            self.positionType = positionType

    #a 3-tuple of positions, used to consider how the state of a row, column or diagonal
    class ThreeInARow:
        def __init__(self, positionOneType, positionTwoType, positionThreeType):
            self.positions = [positionOneType, positionTwoType, positionThreeType]
        
        def IsTheSame(self):
            return (self.positions[0] == self.positions[1] == self.positions[2]) and self.positions[0] != PositionType.BLANK
        def HasAnyOf(self, PositionType):
            return (self.positions[0] == PositionType or self.positions[1] == PositionType or self.positions[2] == PositionType)
        
        def HasTwoTheSame(self):
            xInRow = 0
            oInRow = 0
            for i in self.positions:
                if (i == PositionType.X):
                    xInRow = xInRow + 1
                elif (i == PositionType.O):
                    oInRow = oInRow + 1
            if xInRow == 2:
                return PositionType.X
            elif oInRow == 2:
                return PositionType.O
            else:
                return False

    #gets a row
    def GetRow(self, rowToGet):
        return Board.ThreeInARow(self.GetPositionType(Board.Position(rowToGet, 0)),
                          self.GetPositionType(Board.Position(rowToGet, 1)),
                          self.GetPositionType(Board.Position(rowToGet, 2)))

    #gets a column
    def GetColumn(self, columnToGet):
        return Board.ThreeInARow(self.GetPositionType(Board.Position(0, columnToGet)),
                                 self.GetPositionType(Board.Position(1, columnToGet)),
                                 self.GetPositionType(Board.Position(2, columnToGet)))

    #gets the diag starting at 0,0 to 2,2
    def GetDiag1(self):
        return Board.ThreeInARow(self.GetPositionType(Board.Position(0, 0)),
                                 self.GetPositionType(Board.Position(1,1)),
                                 self.GetPositionType(Board.Position(2,2)))

    #gets the diag starting at 0,2 to 2,0
    def GetDiag2(self):
        return Board.ThreeInARow(self.GetPositionType(Board.Position(0, 2)),
                                 self.GetPositionType(Board.Position(1,1)),
                                 self.GetPositionType(Board.Position(2,0)))


    def __init__(self):
        self.board = [([PositionType.BLANK] * 3)]
        for i in range(2):
            self.board = self.board + [([PositionType.BLANK] * 3)]

    # @return a string describing the result, or False if not finished
    def IsComplete(self):
        for row in range(3):
            if (self.GetRow(row).IsTheSame()):
                return self.board[row][0] + " Won"
        for column in range(3):
            if (self.GetColumn(column).IsTheSame()):
                return self.board[0][column] + " Won"
        if (self.GetDiag1().IsTheSame()):
            return self.board[0][0] + " Won"
        if (self.GetDiag2().IsTheSame()):
            return self.board[2][0] + " Won"
        if (self.AllFilled()):
            return "Draw."
        return False

    def AllFilled(self):
        for i in range(3):
            for j in range(3):
                if (self.GetPositionType(Board.Position(i,j)) == PositionType.BLANK):
                    return False
        return True
            
    #helper function for getting the position type at a position on the board
    def GetPositionType(self, Position):
        return self.board[Position.row][Position.column]

    #mark a move on the board
    def MarkMove(self, Move):
        self.board[Move.position.row][Move.position.column] = Move.positionType; 

    #string streamer for board
    def __str__(self):
        string = "========\n"
        string = string + "  0 1 2\n"
        rowcount = 0
        for i in self.board:
            string =string + str(rowcount) + "|" 
            for j in i:
                string = string + j + "|"
            string  = string + "\n"
            rowcount = rowcount + 1
        return string;


#Abstract Base Class (ABC) Playing Engine
class ABCPlayingEngine(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, PositionType):
        pass
    @abstractmethod
    def PlayingEngineDescription(self):
        pass
    @abstractmethod
    def GetMove(self, board):
        pass

# this is a playing engine that considers moves
# it creates a list of all of the row, column or diags that a position can participate in 
# this is sent to a processing function, which is a parameter specified in the constructor
# that gives each move a priority, with the playing engine choosing the move 
# with the highest priority
class PlayingEngine(ABCPlayingEngine):
    def __init__(self, myPositionType, processingFunction, engineDescription):
        self.engineDescription = engineDescription
        self.processingFunction = processingFunction
        self.myPositionType = myPositionType
        
        if self.myPositionType == PositionType.X:
            self.theirPositionType = PositionType.O
        else:
            self.theirPositionType = PositionType.X

    def PlayingEngineDescription(self):
        return self.engineDescription

    def GetMove(self, board):
        bestPriority = -1
        for  i in range(3):
            for j in range(3):
                if (board.GetPositionType(Board.Position(i,j)) == PositionType.BLANK):
                    position = Board.Position(i,j)
                    if self.IsCorner(position):
                        movePriority = self.ProcessCorner(position, board)
                    elif self.IsSide(position):
                        movePriority = self.ProcessSide(position,board)
                    elif self.IsMiddle(position):
                        movePriority = self.ProcessMiddle(position,board)
                    else:
                        assert False
                    if (movePriority > bestPriority):
                        bestPriority = movePriority
                        bestPosition = Board.Position(i,j)
        return Board.Move(bestPosition, self.myPositionType)
        
    def IsCorner(self,position):
        return ((position.row == 0 or position.row == 2) and 
            (position.column == 0 or position.column == 2))


    def IsSide(self,position):
        return  ((position.row == 1 or position.column == 1) and  (position.column != position.row))


    def IsMiddle(self,position):
        return (position.row == 1 and position.column == 1)

    
    def ProcessCorner(self,position, board):
        cornerRow = board.GetRow(position.row)
        cornerColumn = board.GetColumn(position.column)
        if (position.row != position.column): # its either 0,2 or 2,0
            cornerDiagonal = board.GetDiag2()
        else: #its the corner at 0,0 or 2,2
            cornerDiagonal = board.GetDiag1()
        threeInARows = [cornerRow, cornerColumn, cornerDiagonal];
        return self.processingFunction(threeInARows, self.myPositionType, self.theirPositionType)
        
    def ProcessSide(self,position, board):
        sideRow = board.GetRow(position.row)
        sideColumn = board.GetColumn(position.column)
        threeInARows = [sideRow, sideColumn];
        return self.processingFunction(threeInARows, self.myPositionType, self.theirPositionType)
    
    def ProcessMiddle(self,position, board):
        row = board.GetRow(position.row)
        column = board.GetRow(position.column)
        diagonal = board.GetDiag1()
        diagonal2 = board.GetDiag2()
        threeInARows = [row,column,diagonal,diagonal2]
        return self.processingFunction(threeInARows, self.myPositionType, self.theirPositionType )
    

        
        
    
