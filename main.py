import pygame
import sys

from map import Map

def main():
    pygame.init()
    pygame.display.set_caption("Search algorithms")
    game = Simulation(width=500,height=500, nodeSize=10)
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
        event_key = {
            pygame.K_RETURN:self.search,
            pygame.K_SPACE:self.clear,
            pygame.K_g:self.map.moveGoal,
            pygame.K_r:self.reset,
        }
        event_mouse = {
            pygame.MOUSEBUTTONDOWN:self.action, 
        }
        event_quit = {
            pygame.QUIT:[pygame.quit, sys.exit],  
        }

        for event in pygame.event.get():
            try:
                if event.type in event_quit: # Quit actions
                    [action() for action in event_quit[event.type]]
                            
                if event.type in event_mouse: # Mouse actions
                    event_mouse[event.type]()

                if event.type == pygame.KEYDOWN and event.key in event_key: # Handles keyboard actions
                    event_key[event.key]()
            except: 
                print("Error on key:", event.type)
                    
    def search(self):
        '''Start search using the algorithm'''
        print("search")
    
    def clear(self):
        '''Clear the map'''
        self.map = Map(self,self.nodeSize)
        print("clear map")

    def action(self): 
        print("action")
    
    def reset(self): 
        '''Reset the map'''
        self.map = Map(self,self.nodeSize)
        self.map.generateMap()
        print("reset")

    def draw(self):
        '''Updates the screen'''
        self.map.update()
        pygame.display.update()

    def tick(self):
        '''Update search space'''
        self.ttime = self.clock.tick()
        self.mpos = pygame.mouse.get_pos()

    
if __name__ == "__main__":
    main()