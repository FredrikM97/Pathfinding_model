import pygame
import sys

from map import Map

def main():
    pygame.init()
    pygame.display.set_caption("Search algorithms")
    game = Simulation(width=500,height=500, nodeSize=15)
    game.run()
    
class Simulation():
    def __init__(self,width=500,height=500,nodeSize=15):

        self.clock = pygame.time.Clock()
        self.last_tick = pygame.time.get_ticks()
        self.screen_res = (width, height)
        self.nodeSize = nodeSize
        self.screen = pygame.display.set_mode(self.screen_res, pygame.HWSURFACE, 32)
        self.map = Map(game=self, nodeSize=self.nodeSize)
        
        self.map.generateMap()

        while True:
            self.run()

    def run(self):
        '''Basic functionally of run method'''
        self.events()
        self.tick()
        self.draw()

    def events(self):
        '''Handles all events''' 
        
        event_list = {
            pygame.KEYDOWN:self.key_handler,        
            pygame.MOUSEBUTTONDOWN:self.mouse_handler, 
            pygame.MOUSEBUTTONUP:self.mouse_handler, 
            pygame.MOUSEMOTION:self.mouse_motion_handler,
            pygame.QUIT:self.quit_handler,
        }
   
        for event in pygame.event.get():
            event_list.get(event.type, lambda e:None)(event)                   

    def key_handler(self, event):
        '''Handles key events'''
        event_key = {
            pygame.K_RETURN:self.search,
            pygame.K_SPACE:self.clear,
            pygame.K_g:self.define_Start_Goal,
            pygame.K_r:self.reset,
        }
        event_key.get(event.key, lambda e:None)(event)
        
    def quit_handler(self, event):
        '''Quit game'''
        pygame.quit()
        sys.exit()

    def mouse_handler(self, event):
        '''Update node on position where mouse action happened'''
        self.updateNode(event.pos, event.button, event.type)
        print("action", event.pos, event.button, event.type)
    
    def mouse_motion_handler(self, event):
        '''Update multiple nodes on motion'''
        mouse_state = {
            (1, 0, 0):1,
            (0, 0, 1):3   
        }
        if event.buttons in mouse_state:
            self.updateNode(event.pos, mouse_state[event.buttons], event.type)
    
    def updateNode(self, position:tuple, button:int, inputType:int):
        '''
        Params: 
        *X,Y position of action
        *Button: Right or left button
        *inputType: 5-> Mouse pressed down, 6-> Mouse pressed up 

        Sent data to nodes that should be updated
        TODO: Should contain multiple states for different parts of a node

        Example: Obstacle, Visited, Start, Goal
        '''

        ypos, xpos = position
        node = self.map.nodes[xpos//self.nodeSize][ypos//self.nodeSize]
        
        if self.map.start_goal: # If we want to update the start and goal node
            self.map.start_goal_handler(position, button,inputType)

        else: # Update obstacle of node
            event2state = {
                1:1,
                3:0
            }
            node.nodeState = event2state[button]
            node.update()

    def define_Start_Goal(self, event):
        self.map.start_goal = not self.map.start_goal

    def search(self,event):
        '''Start search using the algorithm'''
        print("search")
    
    def clear(self,event):
        '''Clear the map'''
        self.map = Map(self,self.nodeSize)
        print("clear map")
    
    def reset(self,event): 
        '''Reset the map'''
        self.map = Map(self,self.nodeSize)
        self.map.generateMap()
        print("reset")

    def draw(self):
        '''Updates the screen'''
        pygame.display.update()

    def tick(self):
        '''Update search space'''
        self.ttime = self.clock.tick()
        self.mpos = pygame.mouse.get_pos()

    
if __name__ == "__main__":
    main()