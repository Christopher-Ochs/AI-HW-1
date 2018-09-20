To execute this program run the python script csoSourceCodeFile.py in the commandline interface.  The program will then
prompt you to enter a start state, type or paste into the the CLI in this format x x x x x x x x x x x x x x x x.  Where
each x is a number on the board (Note: the program will not check for duplicate entries).  Repeat this for the goal
state or simply press enter again to use the default goal state 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 0.  There will be a
timeout after 5 min of searching.

A sample output will look like this below:

    ===================================================
    The ID of this board is: f9937f31-0f2a-4b81-a163-21ac760597a6 The parent ID is: 20bc36c4-cca1-4466-a01d-408b50795930
    The G(N) value is: 11
    The H(N) value is: 0
    The F(N) value is: 11

    [1, 2, 3, 4]
    [5, 6, 7, 8]
    [9, 10, 11, 12]
    [13, 14, 15, 0]
    ===================================================

    THERE WILL BE MORE STATES HERE BUT TOOK OUT FOR THIS EXAMPLE

    ===================================================

    The ID of this board is: 0 The parent ID is: 0
    The G(N) value is: 0
    The H(N) value is: 0
    The F(N) value is: 0

    [5, 1, 3, 4]
    [2, 10, 6, 8]
    [13, 9, 7, 12]
    [0, 14, 11, 15]
    ===================================================

    Solution found for the above path using BFS
    Solution fount in 12.653188228607178 seconds
    Number of Moves Required = 12
    Number of Nodes Expanded = 11468
    Number of Nodes in Closed List = 4388
    ===================================================
    ===================================================


The start state will be at the bottom and scroll up to follow the sequence of moves.