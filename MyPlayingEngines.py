from PlayingEngine import * 
from random import *
def GetBestPlayer(positionType):
    return PlayingEngine(positionType, BestPlayerProcessingFunction() , "Best Player" )
    
def GetRealisticPlayer(positionType):
    return PlayingEngine(positionType, RealisticPlayerProcessingFunction(), "Realistic Player")

def GetSimplePlayer(positionType):
    return PlayingEngineStub(positionType)

class BestPlayerProcessingFunction:
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
