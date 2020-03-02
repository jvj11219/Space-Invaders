#Import requried libraries
import sys
import pygame
from time import sleep

#Import settings, ship, alien, button, and bullet
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button

#Import game stats
from game_stats import GameStats

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
        # Create an instance to store game statistics.
        self.stats = GameStats(self)
        #Create an instance of Ship
        self.ship = Ship(self)
        #Create a group of bullets
        self.bullets = pygame.sprite.Group()
        #Create group of aliens
        self.aliens = pygame.sprite.Group()
        #Call reate alien fleet method
        self._create_fleet()
        #Make the Play button.
        self.play_button = Button(self, "Play")
        #Set the background color from Settings
        self.bg_color = (self.settings.bg_color) #Light gray

    def run_game(self):
        #Create infinate looop to run the game
        while True:
            #Call check method to check for events
            self._check_events()
            #Run elements only if game is still active / not lost
            if self.stats.game_active:
                #Call ship's update method for movement
                self.ship.update()
                #Call update bullets method
                self._update_bullets()
                #Call update aliens method
                self._update_aliens()
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
            #Mouse Button Pushed
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

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
        #Check Collisions and Remaining Aliens
        self._check_bullet_alien_collisions()
    
    def _check_bullet_alien_collisions(self):
        #Check for any bullets that have hit aliens
        #If so, get rid of the bullet and the alien
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        #If all aliens destroyed...
        if not self.aliens:
            # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

    def _update_screen(self):
        #Redraw the screen with specified bg_color
        self.screen.fill(self.bg_color)
        #Draw the instance of ship
        self.ship.blitme()
        #Draw bullets list cotents to screen
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        #Draw aliens
        self.aliens.draw(self.screen)
        # Draw the play button if the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()
        #Display the most recently drawn screen
        pygame.display.flip()
    
    def _create_fleet(self):
        #Create the fleet of aliens
        #Create an alien and find the number of aliens in a row
        #Spacing between each alien is equal to one alien width
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        #Determine the number of rows of aliens that fit on the screen.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                            (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Create the full fleet of aliens.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        # Create an alien and place it in the row
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _update_aliens(self):
        #Check if the fleet is at an edge, then update the positions of all aliens in the fleet.
        self._check_fleet_edges()
        #Update the positions of all aliens in the fleet
        self.aliens.update()
        #Look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            #print("Ship hit!!!")
            self._ship_hit()
        #Look for aliens hitting the bottom of the screen
        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        #Respond appropriately if any aliens have reached an edge
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        #Drop the entire fleet and change the fleet's direction
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        #Respond to the ship being hit by an alien
        #Check if ships remain
        if self.stats.ships_left > 0:
            #Decrement ships_left
            self.stats.ships_left -= 1
            #Get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()
            #Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()
            #Pause
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        #Check if any aliens have reached the bottom of the screen
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                #Treat this the same as if the ship got hit.
                self._ship_hit()
                break
    
    def _check_play_button(self, mouse_pos):
        #Start a new game when the player clicks Play
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            #Reset the game settings
            self.settings.initialize_dynamic_settings()
            #Reset the game statistics
            self.stats.reset_stats()
            self.stats.game_active = True
            #Get rid of any remaining aliens and bullets
            self.aliens.empty()
            #Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()
            #Hide the mouse cursor
            pygame.mouse.set_visible(False)

if __name__ == '__main__':
    #Create an instance of AlienInvasion called ai
    ai = AlienInvasion()
    #Run ai
    ai.run_game()