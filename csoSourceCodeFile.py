'''
Christopher Ochs
AI - Assignment 1
TileGame Class
'''

import uuid
from copy import deepcopy
import heapq
import time


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
        print("The ID of this board is: " + str(self.get_id()) + " The parent ID is: " + str(self.get_parent_id()))
        print("The G(N) value is: " + str(self.GN))
        print("The H(N) value is: " + str(self.HN))
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

    # NOTE: Heuristics could be optimized, but discussed with the professor.  Will leave heuristic optimization for
    # later.  Instead a time out function has been implemented for searches that take longer than 5 minutes to complete.
    def heuristic1(self):
        count = 0
        for i in self.get_state():
            if self.GoalState[self.State.index(i)] != i:
                # heuristic could be optimized by adding the cost to move the tile (1-9) or (10-15)
                count = count + 1
        return count

    def heuristic2(self):
        count = 0
        # The index into the list is the (vertical, horizontal) distance from the top left tile
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
def get_start_input(inputStr):
    state = input(inputStr)
    state = state.replace(']', '').replace('[', '').split()
    x = []
    for i in state:
        x.append(int(i))
    if not len(x) == 16:
        print("Input is to correct length!!")
        x = get_start_input(inputStr)
    return x


def get_goal_input(inputStr):
    state = input(inputStr)
    state = state.replace(']', '').replace('[', '').split()
    x = []
    for i in state:
        x.append(int(i))
    return x


# construct the start state list
def construct_state(states):
    x = []
    i = 0
    while i < 16:
        x.append(states[i])
        i = i + 1
    return x


def perform_search(current_board, goal_board):
    # Initialize the open list for the queue
    open_list = []
    # Initialize the closed list
    closed_list = []
    # Add first board to the queue
    heapq.heappush(open_list, (current_board.FN, current_board))

    start_board = deepcopy(current_board)

    # Create start time for timeout
    start_time = time.time()
    # timeout variable
    time_out = False
    final_time = 0
    print("===================================================")
    # Expand when open list is not empty
    while len(open_list) != 0:
        # Check if we found the goal board
        if current_board == goal_board:
            final_time = time.time()-start_time
            break
        # Expand all directions ans ensure board isn't in the closed list
        if current_board not in closed_list:
            if current_board.validate_left():
                heapq.heappush(open_list, (current_board.FN, current_board.move_left()))
            if current_board.validate_down():
                heapq.heappush(open_list, (current_board.FN, current_board.move_down()))
            if current_board.validate_up():
                heapq.heappush(open_list, (current_board.FN, current_board.move_up()))
            if current_board.validate_right():
                heapq.heappush(open_list, (current_board.FN, current_board.move_right()))
            # Add the board to the closed list after expanding
            closed_list.append(current_board)
        # Deep Copy and assign the new current board
        current_board = deepcopy(heapq.heappop(open_list)[1])
        # Ensure it hasn't taken 5 min or longer to expand
        if time.time()-start_time > 300:
            time_out = True
            break

    # Display time out error message
    if time_out:
        print("Error: Time limit for search exceeded")
        if current_board.HNControl == 0:
            print("No solution found for the board using BFS")
        elif current_board.HNControl == 1:
            print("No solution found for the board using A* Heuristic 1")
        else:
            print("No solution found for the board using A* Heuristic 2")
        print(start_board.State[0:4])
        print(start_board.State[4:8])
        print(start_board.State[8:12])
        print(start_board.State[12:16])
    else:
        # Print out the sequence of moves
        count = 1
        while current_board.get_id() != 0:
            current_board.print_board_info()
            for x in closed_list:
                if current_board.get_parent_id() == x.get_id():
                    current_board = deepcopy(x)
                    break
            count = count + 1
        current_board.print_board_info()
        if current_board.HNControl == 0:
            print("Solution found for the above path using BFS")
        elif current_board.HNControl == 1:
            print("Solution found for the above path using A* Heuristic 1")
        else:
            print("Solution found for the above path using A* Heuristic 2")

        print("Solution fount in " + str(final_time) + " seconds")
        print("Number of Moves Required = " + str(count))

    print("Number of Nodes Expanded = " + str(len(open_list) + len(closed_list)))
    print("Number of Nodes in Closed List = " + str(len(closed_list)))
    print("===================================================")
    print("===================================================\n")


def main():
    # get user input
    start_list = get_start_input("Please input the starting state with 16 digits separated by a space: ")
    goal_list = get_goal_input("Please input the goal state with 16 digits separated by a space (enter nothing to use default): ")
    if len(goal_list) == 0:
        goal_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]

    # Do all the types of Searches
    for control in range(0, 3):
        start_state = construct_state(start_list)
        goal_state = construct_state(goal_list)
        current_board = Board(0, 0, start_state, goal_state, control, 0, 0)
        goal_board = Board(-1, -1, goal_state, goal_state, control, 0, 0)

        perform_search(current_board, goal_board)


if __name__ == '__main__':
    main()

