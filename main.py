#!/usr/bin/python3
import getopt,sys
from PlayingEngine import *

def usage():
    print("-r")

def main():
    #playingEngine = ABCPlayingEngine()
    myBoard = Board();
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], "::r", ["help", "output="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print("invalid usage", err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    for o, a in opts:
        if o == "-r":
            verbose = True
            print("using realistic opponent")

if __name__ == "__main__":
    main();
