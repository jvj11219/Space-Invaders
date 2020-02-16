#Import Pygame and Sprite module
import pygame
from pygame.sprite import Sprite

#Create bullet class that inherits from sprite
class Bullet(Sprite):
    #Initalize current instance of the game
    def __init__(self, ai_game):
        #Call super to inherit from sprite
        super().__init__()
        #Set atttributes for screen, settings, and color
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color
        #Create a bullet rectangle at (0, 0) and then set correct position
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        #Set the bullet's midtop to match the ship's midtop
        self.rect.midtop = ai_game.ship.rect.midtop
        #Store a decimal value for the bullet’s y­-coordinate
        self.y = float(self.rect.y)

    #Update bullet atributes
    def update(self):
        #Move bullet up by adjusting y
        self.y -= self.settings.bullet_speed
        #Update the rect position
        self.rect.y = self.y
    
    #Draw the bullet
    def draw_bullet(self):
        #Draw updated bullet atributes to the screen
        pygame.draw.rect(self.screen, self.color, self.rect)