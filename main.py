import numpy as np
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import time

FPS = 120

WIN_HEIGHT = 600
WIN_WIDTH = 800

BLACK = (0, 0, 0)           # Walls
WHITE = (255, 255, 255)     # Grid
GREEN = (0, 255, 0)         # Start Node
RED =   (255, 0, 0)         # End node
BLUE =  (0, 0, 255)         # Parent
LIGHT_BLUE = (18, 231, 255 )# Children Node
YELLOW = (255,255,0)        # Solved root
GREY = (163, 163, 163)      # Separation on the grid

wall_number = -1
start_node_number = 1
end_node_number = 2
child_node_number = 3
parent_node_number = 4
solved_root_number = 5

wall_colour = BLACK
start_node_colour = GREEN
end_node_colour = RED
child_node_colour = LIGHT_BLUE
parent_node_colour = BLUE
solved_root_colour = YELLOW


class Grid:
    def __init__(self, size_of_square):
        self.size = size_of_square
        self.grid = np.full((WIN_HEIGHT//size, WIN_WIDTH//size),0)
        self.grid[0][0] = start_node_number
        self.grid[-1][-1] = end_node_number

        self.start_node = self.get_node_pos(start_node_number)
        self.end_node = self.get_node_pos(end_node_number)

    def get_node_pos(self, number):
        res = np.where(self.grid == number)
        return (res[0][0], res[1][0])


     
    def display(self, win, fill = False, grid = False):
        colours = [WHITE, start_node_colour, end_node_colour, child_node_colour, parent_node_colour, solved_root_colour, wall_colour]


        def fill_white():
            win.fill(WHITE)

        
        def grid_draw():
            rows, columns = self.grid.shape
            for row in range(rows):
                pygame.draw.line(win, GREY, (0, self.size * row), (WIN_WIDTH, self.size*row))

            for column in range(columns):
                pygame.draw.line(win, GREY, (self.size*column, 0), (self.size*column, WIN_HEIGHT))
        
        if fill:
            fill_white()

    
        for indx, number in np.ndenumerate(self.grid):
            
            row = indx[0]
            column = indx[1]
             
            colour = colours[number]
            
            if number != 0:
                pygame.draw.rect(win, colour, (self.size * column, self.size * row, self.size, self.size))
        
        if grid:
            grid_draw()
                
            
    def clear(self, win, walls = False):

        if walls:
            nums = [-1,3,4,5]
        else:
            nums = [3,4,5]

        for indx, value in np.ndenumerate(self.grid):
            if value in nums:
                self.grid[indx[0]][indx[1]] = 0

        refresh_screen(draw = True, update = True, fill = True, Grid = True)
     
    

    def get_pos_on_grid(self, position):
        x,y = position
        result = (y//self.size, x//self.size)
        
        rows, columns = grid.grid.shape

        if 0 <= result[0] < rows and 0 <= result[1] < columns:
            return result
            
        return None
      
    
    def move_node(self, number, position):
        pos_y, pos_x = position
        if self.grid[pos_y][pos_x] not in [1,2] :
            y,x = self.get_node_pos(number)
            self.grid[pos_y][pos_x] = number
            self.grid[y][x] = 0


class Node:
    def __init__(self, parent, position): #position(y,x) -> row,column
        self.parent = parent
        self.position = self.pos = position

        self.gCost = 0
        self.hCost = 0
        self.fCost = 0
        self.length = 0

        if self.parent is not None:
            a = abs(self.pos[0] - end_node.pos[0])
            b = abs(self.pos[1] - end_node.pos[1])

            self.gCost = parent.gCost + ((self.position[0]-parent.position[0])**2 + (self.position[1]-parent.position[1])**2 )**0.5
            self.length = ((self.position[0]-parent.position[0])**2 + (self.position[1]-parent.position[1])**2 )**0.5
            self.hCost = a+b

            self.fCost = self.gCost + self.hCost

    def __eq__(self, others):
        return self.pos == others.pos
    

    def get_children(self, position):
        current_node = self
        n = (0,1,2,3,4,5)
        y, x = position
        down = False
        up = False
        left_up = False
        left_down = False
        right_up = False
        right_down = False
        h_len = len(grid.grid[0])
        v_len = len(grid.grid)
        children = []
        if y < v_len-1:
            y1 = y+1
            x1 = x
            down = True
            if grid.grid[y1][x1] in n:
                children.append(Node(current_node, (y1, x1)))
                left_down = True
                right_down = True

        if y > 0:
            y1 = y-1
            x1 = x
            up = True
            if grid.grid[y1][x1] in n:
                children.append(Node(current_node, (y1, x1)))
                left_up = True
                right_up = True

        if x < h_len-1:
            y1 = y
            x1 = x+1
            if grid.grid[y1][x1] in n:
                children.append(Node(current_node, (y1, x1)))
                right_up = True
                right_down = True

            else:
                right_up = False
                right_down = False
            if right_up and up:
                y1 = y-1
                if grid.grid[y1][x1] in n:
                    children.append(Node(current_node, (y1, x1)))
            if right_down and down:
                y1 = y+1
                if grid.grid[y1][x1] in n:
                    children.append(Node(current_node, (y1, x1)))
        if x > 0:
            y1 = y
            x1 = x-1
            if grid.grid[y1][x1] in n:
                children.append(Node(current_node, (y1, x1)))
                left_up = True
                left_down = True

            if left_up and up:
                y1 = y-1
                if grid.grid[y1][x1] in n:
                    children.append(Node(current_node, (y1, x1)))
            if left_down and down:
                y1 = y+1
                if grid.grid[y1][x1] in n:
                    children.append(Node(current_node, (y1, x1)))

        return children
    

    


def main():
    
    run = True
    editing = False
    deleting = False
    moving = False
    clock = pygame.time.Clock()

    refresh_screen(draw = True, update = True, fill = True, Grid = True)

    
    while run:
        clock.tick(FPS)
        
        pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False 

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_c:
                    grid.clear(win, walls = True)


                elif event.key == pygame.K_SPACE:
                    grid.clear(win, walls = False)
                    print('Running...')
                    start = time.time()
                    length = AStar(win)
                    stop = time.time()

                    if length == -1:
                        print(f'No path found in {round(stop-start, 3)} seconds')
                    elif length == -2:
                        print('The algoright was closed')
                    else:
                        print(f'Path found! It was {round(length*10, 3)} units away from the start node. Solution was found in {round(stop - start, 3)} seconds')
                    
                        
                        

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                pos = grid.get_pos_on_grid(pos)
                if event.button == 1:
            
                    if pos:
                        y,x = pos
                        value = grid.grid[y][x]

                        if value in [-1,3,4,5,0]:
                            editing = True
                        if value in [1,2]:
                            moving = True


                if event.button == 3:
                    mouse_pos = pygame.mouse.get_pos()
                    pos_on_grid = grid.get_pos_on_grid(mouse_pos)

                    if pos_on_grid:
                        y,x = pos_on_grid
                        value = grid.grid[y][x]

                    if value in [-1, 0]:
                        deleting = True


            if event.type == pygame.MOUSEBUTTONUP:
                editing = False
                moving = False
                deleting = False
                


            if moving or editing or deleting:
                pos = pygame.mouse.get_pos()
                pos = grid.get_pos_on_grid(pos)         #y;x -> row;column
                y,x = pos
                if editing:
                    value = grid.grid[y][x]

                    if value in [0,3,4,5,-1]:
                        grid.grid[y][x] = wall_number
                
                if deleting:
                    value = grid.grid[y][x]

                    if value in [-1, 0]:
                        grid.grid[y][x] = 0
                
                if moving:
                    grid.move_node(value, pos)
                    
                grid.display(win, grid = True, fill = True)


            pygame.display.update()

def check_list(list, object):
    try:
        return list.index(object)
    except:
        return -1


def refresh_screen(draw = False, update = False, fill = False, Grid = False):
    if draw:
        grid.display(win, fill = fill, grid = Grid)

    if update:
        pygame.display.update()



def display_root(current_node):
    path = []
    length = 0
    while current_node is not None:
        y,x  = current_node.pos
        if grid.grid[y][x] in (0,3,4,5) and (y,x) != start_node.pos:
            path.append(current_node)
            grid.grid[y][x] = solved_root_number
        length += current_node.length
        current_node = current_node.parent

    refresh_screen(update = True)
   
    return length


def display_found(open_list, closed_list):

    for node in open_list:
        y, x = node.pos
        if grid.grid[y][x] not in [1,2]:
            grid.grid[y][x] = child_node_number


    for node in closed_list:
        y, x = node.pos
        if grid.grid[y][x] not in [1,2]:
            grid.grid[y][x] = parent_node_number

    refresh_screen(draw = True, update=True, fill = False, Grid = True)

   

    




def AStar(win):
    clock = pygame.time.Clock()
    global end_node, start_node
    solve = True

    start_node = Node(None, grid.get_node_pos(start_node_number))
    end_node = Node(None, grid.get_node_pos(end_node_number))

    open_list = [start_node]
    closed_list = []

    start = time.time()
    while solve == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                solve = False
                grid.clear(win, walls = True)
                return -2

        clock.tick(FPS)
        if not open_list:
            solve = False
            return -1

        current_node = min(open_list, key = lambda x: x.fCost)
        current_index = open_list.index(current_node)

        if current_node.pos == end_node.pos:
            solve = False
            break

        children = current_node.get_children(current_node.pos)

        open_list.pop(current_index)
        closed_list.append(current_node)

        for child in children:
            open_list_copy = []
            closed_list_copy = []

            index1 = check_list(open_list, child)
            index2 = check_list(closed_list, child)


            if index1 >= 0 and open_list[index1].fCost > child.fCost:
                open_list.pop(index1)
                open_list.append(child)

            if index1 >= 0 and closed_list[index2].fCost > child.fCost:
                closed_list.pop(index2)
                open_list.append(child)

            if index1 == -1 and index2 == -1:
                open_list.append(child)

        display_found(open_list, closed_list)
    


    length = display_root(current_node)
    refresh_screen(draw = True, Grid = True)
    
    return length


size = 20
if __name__ == '__main__':
    grid = Grid(size)

    win = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
    
    main()
