import numpy as np
class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, direction, parent=None, position=None,):
        self.parent = parent
        self.position = position
        self.direction = direction
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position and self.direction == other.direction

class Direction():
    yList = [-1,-1,0,1,1,1,0,-1]
    xList = [0,-1,-1,-1,0,1,1,1]

    allDirections = False
    #-1,-1,0,1,1,1,0,-1
    #0 is left, 1 is top left, 2 is up, 3 is up right, 4 is right, 5 is bottom right, 6 is down, 7 is down left
    def __init__(self,startDirection):
        if startDirection == 8:
            self.allDirections = True
        self.currentDirection = startDirection
    
    def get_forward_possible_positions(self):
        leftDirection = self.currentDirection-1
        rightDirection = self.currentDirection+1

        if leftDirection < 0:
            leftDirection = 7
        if rightDirection > 7:
            rightDirection = 0
        
        return [(self.xList[leftDirection],self.yList[leftDirection]),
        (self.xList[self.currentDirection],self.yList[self.currentDirection]),
        (self.xList[rightDirection],self.yList[rightDirection])]
    def get_backward_possible_positions(self):
        backDirection = (self.currentDirection+4)%8
        leftDirection = backDirection-1
        rightDirection = backDirection+1

        if leftDirection < 0:
            leftDirection = 7
        if rightDirection > 7:
            rightDirection = 0
        
        return [(self.xList[leftDirection],self.yList[leftDirection]),
        (self.xList[backDirection],self.yList[backDirection]),
        (self.xList[rightDirection],self.yList[rightDirection])]
    def get_next_posible_positions(self):
        positionsF = self.get_forward_possible_positions()
        positionsB = self.get_backward_possible_positions()
        for i in range(0,len(positionsF)):
            positionsB.append(positionsF[i])
        return positionsB
    def position_to_direction(self,x,y):
        for i in range(0,8):
            if self.xList[i] == x and self.yList[i] == y:
                return i

        return 0
    def __eq__(self, other):
        if self.allDirections or other.allDirections:
            return True
        return self.currentDirection == other.currentDirection
    def __str__(self) -> str:
        if self.currentDirection == 0:
            return "Left"
        if self.currentDirection == 1:
            return "UpLeft"
        if self.currentDirection == 2:
            return "Up"
        if self.currentDirection == 3:
            return "UpRight"
        if self.currentDirection == 4:
            return "Right"
        if self.currentDirection == 5:
            return "DownRight"
        if self.currentDirection == 6:
            return "Down"
        if self.currentDirection == 7:
            return "DownLeft"
        return str(self.currentDirection)
        
def astar(maze, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = Node(Direction(4),None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(Direction(8),None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append((current.position,str(current.direction)))
                current = current.parent
            return path[::-1] # Return reversed path

        # Generate children
        children = []
        for new_position in current_node.direction.get_next_posible_positions(): # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(Direction(current_node.direction.position_to_direction(new_position[0],new_position[1])),current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            shouldContinue = True
            for closed_child in closed_list:
                if child == closed_child:
                    shouldContinue = False
                    break
            if not shouldContinue:
                continue
            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    shouldContinue = False
                    break
            if not shouldContinue:
                continue
            # Add the child to the open list
            open_list.append(child)


def convert_directions_for_map(direction):
    if direction == "DownRight" or direction == "UpLeft":
        return "\\"
    if direction == "Up" or direction == "Down":
        return "|"
    if direction == "DownLeft" or direction == "UpRight":
        return "/"
    if direction == "Left" or direction == "Right":
        return "-"
    return "OOPS"

def main():

    maze = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
            [0, 0, 1, 0, 1, 0, 1, 1, 1, 0],
            [0, 0, 1, 0, 1, 1, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 1, 1, 1, 1, 0],
            [0, 0, 1, 1, 0, 1, 0, 0, 0, 1],
            [0, 0, 0, 0, 1, 1, 0, 1, 1, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    start = (0, 0)
    end = (9, 9)

    path = astar(maze, start, end)
    if path is None:
        print("NO SOLUTIONS")
        return

    
    for i in range(0,len(path)):
        if maze[path[i][0][0]][path[i][0][1]] == 0:
            maze[path[i][0][0]][path[i][0][1]] = convert_directions_for_map(path[i][1])
        else:
            maze[path[i][0][0]][path[i][0][1]] = "m"
    print(path)
    print("m = multiple directions (the car visited this spot in different directions)")
    for i in range(0,len(maze)):
        for j in range(0,len(maze[i])):

            print(str(maze[i][j])+" ",end="")
        print()

    #print(maze)


if __name__ == '__main__':
    main()