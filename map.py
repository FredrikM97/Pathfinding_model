import pygame

class Node():
    def __init__(self, map=None, nodeSize=15,pos=None):
        self.map = map
        self.game = self.map.game
        self.nodeSize = nodeSize
        self.pos = pos
        self.blit_pos = [i*nodeSize for i in self.pos]
        self.color = (0,0,0)

        self.image = pygame.Surface((self.nodeSize, self.nodeSize))
        self.rect = self.image.get_rect(topleft=self.blit_pos)

        self.obstacle = False
        self.visited = False
        self.goal = False

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
        if self.visited:
            self.color = self.colors('BLUE')
        else: 
            self.color = self.colors('WHITE')

        if self.obstacle:
            self.color = self.colors('RED')
            
        if self.goal:
            self.color = self.colors('YELLOW')
        
        if pygame.mouse.get_pressed()[0] and self.rect.collidepoint(self.game.mpos):
                self.obstacle = True
                self.color = self.colors('BLACK')

        elif pygame.mouse.get_pressed()[2] and self.rect.collidepoint(self.game.mpos):   
            self.obstacle = False
            self.color = self.colors('WHITE')

    def draw(self, screen):
        self.image.fill(self.color)
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
        self.nodes = [[Node(map=self, nodeSize=self.nodeSize,pos=[row, col]) for row in list(range(0,self.height))] for col in list(range(0,self.width))] 

    def update(self):
        # Update the nodes
        for col in self.nodes:
            for node in col:    
                node.update()
                node.draw(self.game.screen)
        
        # Update the grid
        [pygame.draw.line(self.game.screen, [100]*3, (0, (self.nodeSize*i)), (750, (self.nodeSize*i))) for i in range(0,self.width)]
        [pygame.draw.line(self.game.screen, [100]*3, (self.nodeSize*i, 0), (self.nodeSize*i, 500)) for i in range(0,self.height)]

        
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
                if maze[row][col] == 1: # Obstacle
                    self.nodes[row][col].obstacle = True
                else:
                    self.nodes[row][col].obstacle = False
        
    def moveStart(self):
        '''Move start position'''
        pass
    def moveGoal(self):
        '''Move goal position'''
        pass

    def search(self):
        '''Implement algorithm for search A* etc...'''
        pass