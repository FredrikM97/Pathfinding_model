import pygame
from itertools import product

class Node():
    def __init__(self, map=None, nodeSize=15,pos=None):
        self.map = map
        self.game = self.map.game
        self.nodeSize = nodeSize
        self.pos = pos
        self.blit_pos = [i*nodeSize for i in self.pos]
        self.color = self.colors('WHITE')

        self.image = pygame.Surface((self.nodeSize, self.nodeSize))
        self.rect = self.image.get_rect(topleft=self.blit_pos)

        self.nodeState = 0
        self.nodeStates = {
            0:self.colors('WHITE'),     # Free space
            1:self.colors('RED'),       # Obstacle
            2:self.colors('PURPLE'),    # Start
            3:self.colors('YELLOW'),    # Goal
            4:self.colors('BLUE'),      # Visited
        }

        self.draw(self.game.screen)

    def colors(self, colorType):
        color = {
            'BLACK':    (0, 0, 0),
            'WHITE':    (255, 255, 255),
            'BLUE':     (0, 0, 255),
            'RED':      (255, 0, 0),
            'YELLOW':   (255, 255, 0),
            'GREEN':    (0, 255, 0),
            'ORANGE':   (255, 165, 0),
            'PURPLE':   (255, 0, 255),
        }
        return color[colorType]

    def update(self):
        self.color = self.nodeStates[self.nodeState]
        self.draw(self.game.screen)

    def draw(self, screen):
        self.image.fill(self.color)

        coords = [*product((0, self.nodeSize),(0, self.nodeSize))]
        coord_index = [(0,1),(1,3),(3,2),(2,0)]
        [pygame.draw.line(self.image, [100]*3, coords[start], coords[end]) for start, end in coord_index] 

        screen.blit(self.image, self.rect)

        

class Map:
    '''
    Define how the map will look like
    '''
    def __init__(self, game=None, nodeSize=15):
        self.game = game
        self.nodeSize = nodeSize

        self.width = int((self.game.screen_res[1]/self.nodeSize))
        self.height = int(self.game.screen_res[0]/self.nodeSize) 
        self.nodes = [[Node(map=self, nodeSize=self.nodeSize,pos=[row,col]) for row in list(range(self.height))] for col in list(range(self.width))] 

        self.genererateGrid()
        self.start_goal = False
        self.statePositions = [(),()] # Remember nodes that contain start/goal position

    def update(self):
        pass
        
    def genererateGrid(self):
         # Update the grid (Surface, color, start, end)
        [pygame.draw.line(self.game.screen, [100]*3, (0, (self.nodeSize*i)), (self.width*self.nodeSize, (self.nodeSize*i))) for i in range(0,self.width)]
        [pygame.draw.line(self.game.screen, [100]*3, (self.nodeSize*i, 0), (self.nodeSize*i, self.height*self.nodeSize)) for i in range(0,self.height)]

    def generateMap(self):
        '''Generates a map of given size with obstacles'''
        
        width = 10
        height = 8
        maze = [[1,1,1,1,1,1,1,1,1,1],
                [1,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,1],
                [1,0,1,1,1,1,1,1,0,1],
                [1,0,1,0,0,0,0,0,0,1],
                [1,0,1,0,1,1,1,1,0,1],
                [1,0,0,0,0,0,0,0,0,1],
                [1,1,1,1,1,1,1,1,1,1]]
        
        for col,_ in enumerate(maze[0]):
            for row,_ in enumerate(maze): 
                node = self.nodes[row][col]
                node.nodeState = maze[row][col] # If 1: Obstacle, 0: Free -> Check nodeState
                node.update()
        
    def start_goal_handler(self,position:tuple, button:int,inputType:int):
        '''
        Define start & goal position
        Start: Left button -> 1
        Goal: Right button -> 3
        '''
        state2index = {
            1:0, # Start
            3:1  # Goal
        }
        
        # Remove old start/goal
        if len(self.statePositions[state2index[button]]):
            ypos, xpos = self.statePositions[state2index[button]]
            node_0 = self.nodes[xpos//self.nodeSize][ypos//self.nodeSize]

            node_0.nodeState = 0 # Mark node as free
            node_0.update()

        # Change to new position
        state2int = {
            1:2, # Start
            3:3  # Goal
        }
        ypos, xpos = position
        node_1 = self.nodes[xpos//self.nodeSize][ypos//self.nodeSize]
        
        node_1.color = node_1.nodeStates[state2int[button]]
        if inputType == 6:
            node_1.nodeState = state2int[button]
            # TODO: Only update when dropping mouse
        
        node_1.draw(self.game.screen)

        self.statePositions[state2index[button]] = (ypos,xpos)
        
 

    def search(self):
        '''Implement algorithm for search A* etc...'''
        pass