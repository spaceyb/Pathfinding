#!/usr/bin/env Python3
from operator import truediv
import pygame
from math import floor
from operator import attrgetter

# Application Name
APP_NAME = "Lee's Algorithm"

# Screen Parameters
SCREEN_X = 800
SCREEN_Y = 600

# Grid Parameters
COLUMNS = 80
ROWS = 60

# Box Parameters
BOX_WIDTH = SCREEN_X / COLUMNS
BOX_HEIGHT = SCREEN_Y / ROWS

# Define Colours
BLACK = 0,0,0
WHITE = 255,255,255
RED = 255,0,0
GREEN = 0,255,0
BLUE = 0,0,255
YELLOW = 255,255,0
PINK = 255,20,147


# Define list to hold Box Data
grid = []
path = []
search = []
currentSearch = []

# Variables to handle game states
bPathFound = False
bBacktrackPathFound = False

# Class to represent a box 
class Box:
    def __init__(self, i, j):
        self.x = i
        self.y = j
        self.wall = False
        self.start = False
        self.end = False
        self.path = False
        self.searching = False
        self.discovered = False
        self.distance = 0

    def draw(self, win, colour):
        pygame.draw.rect(win, colour, (self.x * BOX_WIDTH, self.y * BOX_HEIGHT, BOX_WIDTH - 2, BOX_HEIGHT - 2))

# Create the Grid
def createGrid():
    for i in range(COLUMNS):
        newArray = []
        for j in range(ROWS):
            newArray.append(Box(i,j))
        grid.append(newArray)

def findPath():
   # Search adjacent boxes to query legitimate moves
    while search:
        box = search.pop()
        # Search North
        if box.y - 1 >= 0 and not (grid[box.x][box.y - 1].discovered or grid[box.x][box.y - 1].wall):
            if queryPathFound(grid[box.x][box.y - 1]):
                bPathFound = True
                break
            grid[box.x][box.y - 1].searching = True
            grid[box.x][box.y - 1].discovered = True
            grid[box.x][box.y - 1].distance = box.distance + 1
            currentSearch.append(grid[box.x][box.y - 1])     
        # Search South
        if box.y + 1 < ROWS and not (grid[box.x][box.y + 1].discovered or grid[box.x][box.y + 1].wall):
            if queryPathFound(grid[box.x][box.y + 1]):
                bPathFound = True
                break
            grid[box.x][box.y + 1].searching = True
            grid[box.x][box.y + 1].discovered = True
            grid[box.x][box.y + 1].distance = box.distance + 1
            currentSearch.append(grid[box.x][box.y + 1])   
        # Search East
        if box.x + 1 < COLUMNS and not (grid[box.x + 1][box.y].discovered or grid[box.x + 1][box.y].wall):
            if queryPathFound(grid[box.x + 1][box.y]):
                bPathFound = True
                break
            grid[box.x + 1][box.y].searching = True
            grid[box.x + 1][box.y].discovered = True
            grid[box.x + 1][box.y].distance = box.distance + 1
            currentSearch.append(grid[box.x + 1][box.y])
        # Search West
        if box.x - 1 >= 0 and not (grid[box.x - 1][box.y].discovered or grid[box.x - 1][box.y].wall):
            if queryPathFound(grid[box.x - 1][box.y]):
                bPathFound = True
                break
            grid[box.x - 1][box.y].searching = True
            grid[box.x - 1][box.y].discovered = True
            grid[box.x - 1][box.y].distance = box.distance + 1
            currentSearch.append(grid[box.x - 1][box.y])
        
    while currentSearch:
        tempbox = currentSearch.pop()
        search.append(tempbox)

def queryPathFound(box):
    global bPathFound
    if box.end:
        bPathFound = True
        return True
    else:
        return False

def backtrackPath():
    global bBacktrackPathFound
    # Backtract to find the path
    temppath = []
    while path:
        node = path.pop()
        # Find the lowest value around the node
        # Check North
        if node.y - 1 >= 0 and grid[node.x][node.y - 1].distance or grid[node.x][node.y - 1].start:
            temppath.append(grid[node.x][node.y - 1])
        # Check South
        if node.y + 1 < ROWS and grid[node.x][node.y + 1].distance or grid[node.x][node.y + 1].start:
            temppath.append(grid[node.x][node.y + 1])
        # Check East
        if node.x + 1 < COLUMNS and grid[node.x + 1][node.y].distance or grid[node.x + 1][node.y].start:
            temppath.append(grid[node.x + 1][node.y])
        # Check West
        if node.x - 1 >= 0 and grid[node.x - 1][node.y].distance or grid[node.x - 1][node.y].start:
            temppath.append(grid[node.x - 1][node.y])

    # Find the lowest distance and assign to the path
    if len(temppath):
        lowest = min(temppath, key=attrgetter('distance')) 
        lowest.path = True
        path.append(lowest)

    if path[0].start:
        bBacktrackPathFound = True

    

def main():
    # Initialise Pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))
    pygame.display.set_caption(APP_NAME)

    createGrid()

    bGameRunning = True
    bStartSet = False
    bEndSet = False
    bStartPathfinding = False

    global bPathFound

    while bGameRunning:
        # Loop through pygame events
        for event in pygame.event.get():
            # Check for KEYDOWN Event
            if event.type == pygame.KEYDOWN:
                #Exit if the backspace key is pressed
                if event.key == pygame.K_BACKSPACE:
                    bGameRunning = False
                elif event.key == pygame.K_SPACE and bStartSet and bEndSet and not bStartPathfinding:
                    bStartPathfinding = True
            # Mouse Controls
            elif not bStartPathfinding and event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Set Start Index
                    if not bStartSet:
                        i = floor(x / BOX_WIDTH)
                        j = floor(y / BOX_HEIGHT)
                        grid[i][j].start = True
                        grid[i][j].discovered = True
                        bStartSet = True
                        search.append(grid[i][j])
                    # Set End Index
                    elif not bEndSet:
                        i = floor(x / BOX_WIDTH)
                        j = floor(y / BOX_HEIGHT)
                        grid[i][j].end = True
                        bEndSet = True
                        path.append(grid[i][j])
            elif not bStartPathfinding and event.type == pygame.MOUSEMOTION:
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]
                # Left Click
                if event.buttons[1]:
                    i = floor(x / BOX_WIDTH)
                    j = floor(y / BOX_HEIGHT)
                    grid[i][j].wall = True   
                    grid[i][j].disovered = True                     
            # Check for QUIT event
            elif event.type == pygame.QUIT:
                bGameRunning = False

        # Reset the screen
        screen.fill(BLACK)

        # Find the path
        if bStartPathfinding and not bPathFound:
            findPath()
        
        # Backtrack the path
        if bPathFound and not bBacktrackPathFound:
            backtrackPath()

        # Draw the updated grid
        for i in range(COLUMNS):
            for j in range(ROWS):
                box = grid[i][j]
                # Draw Box
                if box.wall == True:
                    box.draw(screen, RED)
                elif box.start == True:
                    box.draw(screen, GREEN)
                elif box.end == True:
                    box.draw(screen, BLUE)
                elif box.searching:
                    box.draw(screen, YELLOW)
                    box.searching = False
                elif box.path:
                    box.draw(screen, PINK)
                elif box.discovered:
                    box.draw(screen, YELLOW)
                else:  
                    box.draw(screen, (i,j,0))

        pygame.display.update()
      
if __name__ == '__main__':
    main()