'''
Christopher Ochs
AI - Assignment 1
TileGame Class
'''

import uuid
from copy import deepcopy
import heapq

# Board class will handle states, IDs, cost values, asd heuristics
class Board:
    def __init__(self, id, parentID, state, goalState, control, gn, hn):
        self.ID = id
        self.ParentID = parentID
        self.State = state
        self.GoalState = goalState
        # HNControl if 0 run Breadth First, if 1 use Heuristic 1, if 2 run Heuristic 2
        self.HNControl = control
        self.GN = gn
        self.HN = hn
        self.FN = self.GN + self.HN

    # Need to overload less than so the heap Queue will sort itself
    def __lt__(self, other):
        return self.FN < other.FN

    # Overload the equals operator to compare states between Boards rather than memory adresses
    def __eq__(self, other):
        x = self.get_state()
        y = other.get_state()
        for i in range(0, 16):
            if x[i] != y[i]:
                return False
        return True

    # Getter method for ID
    def get_id(self):
        return self.ID

    # Getter method for Parent ID
    def get_parent_id(self):
        return self.ParentID

    # Getter method for goal state
    def get_goal_state(self):
        return self.GoalState

    # Getter method for state
    def get_state(self):
        return self.State

    # Prints out the state of the board in a 4x4 matrix
    def print_state(self):
        print(self.State[0:4])
        print(self.State[4:8])
        print(self.State[8:12])
        print(self.State[12:16])
        print("===================================================\n")

    # Print out all necessary board information
    def print_board_info(self):
        print("The ID of this board is: " + str(self.get_id()) + "\n")
        print("The G(N) value is: " + str(self.GN) + "\n")
        print("The H(N) value is: " + str(self.HN) + "\n")
        print("The F(N) value is: " + str(self.FN) + "\n")
        self.print_state()

    # Returns True if an up move can be performed, False if otherwise.
    def validate_up(self):
        i = self.State.index(0)
        if i not in [0, 1, 2, 3]:
            return True
        return False

    # Performs the move up operation on the state of the current board
    def move_up(self):
        # Get index of 0 value
        indx = self.State.index(0)
        # Deep copy the state to get a true copy of the state
        newState = deepcopy(self.State)
        # Get the value of what tile we are moving
        valueIndex = newState[indx - 4]
        # Perform the switch
        newState[indx] = valueIndex
        newState[indx - 4] = 0
        return self.create_new_board(newState, valueIndex)


    def validate_down(self):
        i = self.State.index(0)
        if i not in [12, 13, 14, 15]:
            return True
        return False

    def move_down(self):
        indx = self.State.index(0)
        newState = deepcopy(self.State)
        valueIndex = newState[indx + 4]
        newState[indx] = valueIndex
        newState[indx + 4] = 0
        return self.create_new_board(newState, valueIndex)

    def validate_left(self):
        i = self.State.index(0)
        if i not in [0, 4, 8, 12]:
            return True
        return False

    def move_left(self):
        indx = self.State.index(0)
        newState = deepcopy(self.State)
        valueIndex = newState[indx - 1]
        newState[indx] = valueIndex
        newState[indx - 1] = 0
        return self.create_new_board(newState, valueIndex)

    def validate_right(self):
        i = self.State.index(0)
        if i not in [3, 7, 11, 15]:
            return True
        return False

    def move_right(self):
        indx = self.State.index(0)
        newState = deepcopy(self.State)
        valueIndex = newState[indx + 1]
        newState[indx] = valueIndex
        newState[indx + 1] = 0
        return self.create_new_board(newState, valueIndex)

    def create_new_board(self, newState, valueIndex):
        # Determine which heuristic we want to use:
        # 0 is BFS
        # 1 is A* using heuristic 1
        # 2 is A* using heuristic 2
        if self.HNControl == 0:
            # Return new board object with a new unique ID, assign the corresponding parent ID, give the updated
            # state list, pass the same goal state and Heuristic Control, calculate the new GN value, and keep
            # the HN value the same since it is not implemented with BFS.
            return Board(uuid.uuid4(), self.ID, newState, self.GoalState, self.HNControl, (self.GN + 1), self.HN)
        # Use Heuristic 1
        elif self.HNControl == 1:
            # Determine size of the size of the tile we are moving and add the corresponding cost to the GN value
            if valueIndex > 9:
                return Board(uuid.uuid4(), self.ID, newState, self.GoalState, self.HNControl, (self.GN + 10),
                             self.heuristic1())
            else:
                return Board(uuid.uuid4(), self.ID, newState, self.GoalState, self.HNControl, (self.GN + 1), self.heuristic1())
        # use heuristic 2
        else:
            # Determine size of the size of the tile we are moving and add the corresponding cost to the GN value
            if valueIndex > 9:
                return Board(uuid.uuid4(), self.ID, newState, self.GoalState, self.HNControl, (self.GN + 10),
                             self.heuristic2())
            else:
                return Board(uuid.uuid4(), self.ID, newState, self.GoalState, self.HNControl, (self.GN + 1), self.heuristic2())

    def heuristic1(self):
        count = 0
        for i in self.get_state():
            if self.GoalState[self.State.index(i)] != i:
                count = count + 1
        return count

    def heuristic2(self):
        count = 0
        position = [(0, 0), (0, 1), (0, 2), (0, 3),
                    (1, 0), (1, 1), (1, 2), (1, 3),
                    (2, 0), (2, 1), (2, 2), (2, 3),
                    (3, 0), (3, 1), (3, 2), (3, 3)]
        for i in self.State:
            indx = self.State.index(i)
            goalIndx = self.GoalState.index(i)
            count += abs(position[indx][0] - position[goalIndx][0])
            count += abs(position[indx][1] - position[goalIndx][1])
        return count


# Modify the input removing braces and converting to list of integers
def getInput(inputStr):
    state = input(inputStr)
    state = state.replace(']', '').replace('[', '').split()
    x = []
    for i in state:
        x.append(int(i))
    return x


# construct the start state list
def constructState(states):
    x = []
    i = 0
    while i < 16:
        x.append(states[i])
        i = i + 1
    return x


def performSearch(currentBoard, goalBoard):
    openList = []
    heapq.heappush(openList, (currentBoard.FN, currentBoard))
    closedList = []
    while len(openList) != 0:
        if currentBoard == goalBoard:
            break
        if currentBoard not in closedList:
            if currentBoard.validate_left():
                heapq.heappush(openList, (currentBoard.FN, currentBoard.move_left()))
            if currentBoard.validate_down():
                heapq.heappush(openList, (currentBoard.FN, currentBoard.move_down()))
            if currentBoard.validate_up():
                heapq.heappush(openList, (currentBoard.FN, currentBoard.move_up()))
            if currentBoard.validate_right():
                heapq.heappush(openList, (currentBoard.FN, currentBoard.move_right()))
            closedList.append(currentBoard)
        currentBoard = deepcopy(heapq.heappop(openList)[1])

    count = 1
    while currentBoard.get_id() != 0:
        currentBoard.print_board_info()
        for x in closedList:
            if currentBoard.get_parent_id() == x.get_id():
                currentBoard = deepcopy(x)
                break
        count = count + 1

    currentBoard.print_board_info()
    print("Number of Moves Required = " + str(count))
    print("Number of Nodes in Search Process List = " + str(len(openList) + len(closedList)))
    print("Number of Nodes in Closed List = " + str(len(closedList)))


def main():
    # get user input
    #startList = getInput("Please input the starting state with 16 digits separated by a space: ")
    #goalList = getInput("Please input the goal state with 16 digits separated by a space: ")

    #startList = [1, 0, 3, 4, 5, 2, 7, 8, 9, 6, 15, 11, 13, 10, 14, 12]
    startList = [5, 1, 3, 4, 2, 10, 6, 8, 13, 9, 7, 12, 0, 14, 11, 15]
    goalList = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]
    startState = constructState(startList)
    goalState = constructState(goalList)
    currentBoard = Board(0, 0, startState, goalState, 2, 0, 0)
    goalBoard = Board(-1, -1, goalState, goalState, 2, 0, 0)

    performSearch(currentBoard, goalBoard)


if __name__ == '__main__':
    main()

