#Import requried libraries
import sys
import pygame

#Import settings
from settings import Settings

#Create overall class to manage game assets and behaviors
class AlienInvasion:
    def __init__(self):
        #Initalize game and required resources
        pygame.init()
        self.settings = Settings()
        #Create a game window (surface) with values from Settings
        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_width))
        #Name the window Alien Invasion
        pygame.display.set_caption("Alien Invasion")
        #Set the background color from Settings
        self.bg_color = (self.settings.bg_color) #Light grey

    def run_game(self):
        #Create infinate looop to run the game
        while True:
            #Check for keyboard/mouse events
            for event in pygame.event.get():
                #Quit event (user clicks close on the window)
                if event.type == pygame.QUIT:
                    sys.exit()
            #Redraw the screenw with specified bg_color
            self.screen.fill(self.bg_color)
            #Display the most recently drawn screen
            pygame.display.flip()

if __name__ == '__main__':
    #Create an instance of AlienInvasion called ai
    ai = AlienInvasion()
    #Run ai
    ai.run_game()