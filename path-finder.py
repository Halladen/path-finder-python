import curses    # pipi install windows-curses
from curses import wrapper
import queue
import time

#curses used to visualize the implementation to the terminal


# "#" means obstacles in the maze
# empty strings are things that we can navigate
# "O" is start 
# "X" is end

maze = [
    ["#", "O", "#", "#", "#", "#", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", "#", " ", "#", "#", " ", "#"],
    ["#", " ", "#", " ", " ", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "X", "#"]
]

def print_maze(maze,stdscr,path=[]):
    BLUE = curses.color_pair(1)
    RED = curses.color_pair(2)

    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if (i,j) in path:
                stdscr.addstr(i,j*2,"X" ,RED)
            else:
                stdscr.addstr(i,j*2,value ,BLUE)  # "j*2" put more spases between values

def find_start(maze,start):
    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if value == start:
                return i,j  # return the row "i" and the column "j"
    return None

def find_path(maze , stdscr):
    start = "O"
    end = "X"
    start_pos = find_start(maze,start)

    q = queue.Queue()
    q.put((start_pos,[start_pos])) # position we are currently on and the path 
    visited = set()

    while not q.empty():
        current_pos, path = q.get()
        row,col = current_pos

        stdscr.clear()
        print_maze(maze,stdscr,path)
        time.sleep(0.2)
        stdscr.refresh()
        

        if maze[row][col] == end:
            return path
        
        neighbors = find_neighbors(maze,row,col)
        for neighbor in neighbors:
            if neighbor in visited:
                continue
            r,c = neighbor
            if maze[r][c] == "#":
                continue

            new_path = path + [neighbor]
            q.put((neighbor,new_path))
            visited.add(neighbor)

        
def find_neighbors(maze,row,col):
    neighbors = []
    if row > 0: # up
        neighbors.append((row - 1,col))
    if row + 1 < len(maze): #down
        neighbors.append((row + 1,col))
    if col > 0 : # left
        neighbors.append((row,col - 1))
    if col + 1 < len(maze): # right
        neighbors.append((row,col + 1))
    return neighbors

def main(stdscr):   # stdscr stands for standard output screen
    # initialize the foreground and background colors 
    # 1 is for pair id
    curses.init_pair(1,curses.COLOR_BLUE,curses.COLOR_BLACK) 
    curses.init_pair(2,curses.COLOR_RED,curses.COLOR_BLACK) 
    # using the color that we initialized with id 1
    blue_and_black = curses.color_pair(1)


    find_path(maze,stdscr)
    stdscr.getch()  #to get input

wrapper(main)   # initialize the curses module for as then call the function