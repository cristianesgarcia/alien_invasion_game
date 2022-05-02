# Cristiane -- 11/04/22

import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represent a simple alien in the fleet."""
    def __init__(self, alien_invasion_game):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.screen = alien_invasion_game.screen
        self.settings = alien_invasion_game.settings

        # Load the alien image and set its rect attribute.
        self.alien_image_path = 'images/alien.bmp'
        self.image = pygame.image.load(self.alien_image_path)
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact horizontal position.
        self.x = float(self.rect.x)
    
    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
    
    def update(self):
        """Move the alien to the right or left."""
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x
