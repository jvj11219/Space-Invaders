#Create a class to store all the game settings
class Settings:
    #Initialize game settings
    def __init__(self):
        #Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230,230,230)
        #Ship settings
        self.ship_speed = 20
        self.ship_limit = 3
        #Bullet settings
        self.bullet_speed = 30.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60) #Dark gray
        self.bullets_allowed = 3
        #Alien settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        #Fleet_direction of 1 represents right and -1 represents left
        self.fleet_direction = 1