from PlayingEngine import * 
from random import *


def GetBestPlayer(positionType):
    return PlayingEngine(positionType, BestPlayerProcessingFunction() , "Best Player" )

def GetRealisticPlayer(positionType):
    return PlayingEngine(positionType, RealisticPlayerProcessingFunction(), "Realistic Player")

def GetSimplePlayer(positionType):
    return PlayingEngineStub(positionType)

class BestPlayerProcessingFunction:
    # each move in tic tac toe can be compared against others 
    # by the number of still available row, column or diagonals
    # that the move can participate in
    # 
    # however, there is also a priority in the cases when either 
    # of the players has an opportunity to win the game
    # if I have a move that can win me the game, I MUST take it
    # else if they have an opportunity to win the game, I MUST prevent
    # them from winning.
    # In both of these cases, I must choose a specific position as 
    # opposed to searching for an optimal move for myself described 
    # in the paragraph above 
    def __call__(self, threeInARows, myPositionType, theirPositionType):
        participateCount = 0
        priority = 0
        for threeInARow in threeInARows:
            hasTwoTheSame = threeInARow.HasTwoTheSame();
            if (hasTwoTheSame):
                if (hasTwoTheSame == myPositionType):
                    priority  = 6 #we won, will choose ths one 
                    return priority
                elif (hasTwoTheSame == theirPositionType):
                    priority = max(priority, 5) #will choose this if we cannot win
            elif (threeInARow.HasAnyOf(theirPositionType) == False):
                    participateCount = participateCount + 1 #note that we can still participate using this move
        return max(participateCount, priority)

#when it has an opportunity to win, it flips a coin to decide whether or not to take the win
class RealisticPlayerProcessingFunction:
    def __call__(self, threeInARows, myPositionType, theirPositionType):
        participateCount = 0
        priority = 0
        for threeInARow in threeInARows:
            hasTwoTheSame = threeInARow.HasTwoTheSame();
            if (hasTwoTheSame):
                if (hasTwoTheSame == myPositionType):
                    if (randint(0,1) == 1):
                        priority = 6
                        return priority
                elif (hasTwoTheSame == theirPositionType):
                    priority = max(priority, 5) #will choose this if we cannot win
            elif (threeInARow.HasAnyOf(theirPositionType) == False):
                    participateCount = participateCount + 1 #note that we can still participate using this move
        return max(participateCount, priority)
    
#this is a simple player that just returns the first one it finds that is blank
class PlayingEngineStub(ABCPlayingEngine):
    def __init__(self, PositionType):
        self.myPositionType = PositionType
    def PlayingEngineDescription(self, board):
        return "An Empty Stub Playing Engine"
    def GetMove(self, board):
        for i in range(3):
            for j in range(3):
                if (board.GetPositionType(Board.Position(i,j)) == PositionType.BLANK):
                    return Board.Move(Board.Position(i,j), self.myPositionType)
