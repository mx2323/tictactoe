#!/usr/bin/python3
import getopt,sys
from MyPlayingEngines import *
from random import *
def usage():
    print("-r")

def main():
    if (len(sys.argv) == 2 and sys.argv[1] == "realistic"):
        playingEngine = GetRealisticPlayer(PositionType.X)
    elif (len(sys.argv) == 2 and sys.argv[1] == "simple"):
        playingEngine = GetSimplePlayer(PositionType.X)
    else:
        playingEngine = GetBestPlayer(PositionType.X)
        
    myBoard = Board();

    turnCount = randint(0,1);
    print("Playing against " + playingEngine.PlayingEngineDescription())
    print(myBoard)
    while (myBoard.IsComplete() == False):
        if (turnCount % 2 == 0):
            print("X'S Turn\n")
            myBoard.MarkMove(playingEngine.GetMove(myBoard))
        else:
            print("O's Turn\n")
            name = input("Enter Your Move. Separate by a comma. I.E: 1,2\n")
            OPosition = str.split(name, ",")
            myBoard.MarkMove(Board.Move(Board.Position(int(OPosition[0]), int(OPosition[1])), PositionType.O))
        print(myBoard)                               
        turnCount = turnCount + 1
        
    print(myBoard.IsComplete())

if __name__ == "__main__":
    main();
