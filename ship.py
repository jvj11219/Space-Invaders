#Import library
import pygame

#Create a class to manage the ship
class Ship:
    #Define method of Ship to include self reference and current game instance
    def __init__(self,ai_game):
        #Initialize the ship and set its starting position
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        #Load ship settings
        self.settings = ai_game.settings
        #Load the ship image and set its rectangle (rect)
        self.image = pygame.image.load("images/ship.bmp")
        self.rect = self.image.get_rect()
        #Start each new ship at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom
        #Store a decimal value for the ship's horizonal position
        self.x = float(self.rect.x)
        #Movement flags
        self.moving_right = False
        self.moving_left = False
    
    #Create update method for ship's continuous movement
    def update(self):
        #If moving right flag is True and is in bounds
        if self.moving_right and self.rect.right < self.screen_rect.right:
            #Increase ship's x by 1 when moving right
            self.x += self.settings.ship_speed
        #If moving left flag is True and is in bounds
        if self.moving_left and self.rect.left > 0:
            #Decrease ship's x by 1 when moving left
            self.x -= self.settings.ship_speed
        #Update the ship's rect based on ship.x value
        self.rect.x = self.x


    def blitme(self):
        #Draw the ship at its current location
        self.screen.blit(self.image,self.rect)

