#Import requried libraries
import sys
import pygame

#Import settings, ship, and bullet
from settings import Settings
from ship import Ship
from bullet import Bullet

#Create overall class to manage game assets and behaviors
class AlienInvasion:
    def __init__(self):
        #Initalize game and required resources
        pygame.init()
        self.settings = Settings()
        #Change display settings to run at full-screen
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height
        #Create a game window (surface) with values from Settings
        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        #Name the window Alien Invasion
        pygame.display.set_caption("Alien Invasion")
        #Create an instance of Ship
        self.ship = Ship(self)
        #Creat a group of bullets
        self.bullets = pygame.sprite.Group()
        #Set the background color from Settings
        self.bg_color = (self.settings.bg_color) #Light gray

    def run_game(self):
        #Create infinate looop to run the game
        while True:
            #Call check method to check for events
            self._check_events()
            #Call ship's update method for movement
            self.ship.update()
            #Call update bullets method
            self._update_bullets()
            #Call update method to update screen
            self._update_screen()
            #Print the number of bullets on the screen
            print(len(self.bullets))


    def _check_events(self):
        #Check for keyboard/mouse events
        for event in pygame.event.get():
            #Quit event (user clicks close on the window)
            if event.type == pygame.QUIT:
                sys.exit()
            #Key pressed down
            elif event.type == pygame.KEYDOWN:
                #Call keydown method
                self._check_keydown_events(event)
            #Key unpressed
            elif event.type == pygame.KEYUP:
                #Call keyup method
                self._check_keyup_events(event)

    def _check_keydown_events(self,event):
        #Right arrow key (move right)
        if event.key == pygame.K_RIGHT:
            #Move ship right by setting moving_right flag to true
            self.ship.moving_right = True
        #Left arrow key (move left)
        if event.key == pygame.K_LEFT:
            #Move ship left by setting moving_left flag to true
            self.ship.moving_left = True
        #Q key (quit)
        elif event.key == pygame.K_q:
            #Exit game
            sys.exit()
        #Space key (fire bullet)
        elif event.key == pygame.K_SPACE:
            #Fire bullet from ship by calling fire bullet method
            self._fire_bullet()

    def _fire_bullet(self):
        #If num bullets is less than max allowed
        if len(self.bullets) < self.settings.bullets_allowed:
            #Create new bullet
            new_bullet = Bullet(self)
            #Add new bullet to the bullets group
            self.bullets.add(new_bullet)

    def _check_keyup_events(self,event):
        #Right arrow key
        if event.key == pygame.K_RIGHT:
            #Stop moving ship right by setting moving_right flag to flase
            self.ship.moving_right = False
        #Left arrow key
        if event.key == pygame.K_LEFT:
            #Stop moving ship left by setting moving_left flag to flase
            self.ship.moving_left = False

    def _update_bullets(self):
        #Call the bullet's update method
        self.bullets.update()
        #Get rid of bullets that are off screen
        for bullet in self.bullets.copy():
            #If bullet is off the screen
            if bullet.rect.bottom <= 0:
                #Remove from bullets list
                self.bullets.remove(bullet)
    
    def _update_screen(self):
        #Redraw the screen with specified bg_color
        self.screen.fill(self.bg_color)
        #Draw the instance of ship
        self.ship.blitme()
        #Draw bullets list cotents to screen
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        #Display the most recently drawn screen
        pygame.display.flip()

if __name__ == '__main__':
    #Create an instance of AlienInvasion called ai
    ai = AlienInvasion()
    #Run ai
    ai.run_game()