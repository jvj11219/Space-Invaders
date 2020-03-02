#Import pygame and sprites
import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    #Create a class to make aliens
    def __init__(self, ai_game):
    #Initalize alien and set a starting point
        super().__init__()
        self.screen = ai_game.screen
        #Load the alien image and set its rect attribute
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()
        #Start each new alien near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        #Store the alien's horizontal position
        self.x = float(self.rect.x)