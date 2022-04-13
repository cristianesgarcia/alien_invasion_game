# Cristiane -- 08/04/22

import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """A class to manage the ship."""

    def __init__(self, alien_invasion_game, size='normal'):
        """Initialize the ship and set its start position."""
        super().__init__()
        self.screen = alien_invasion_game.screen
        self.screen_rect = alien_invasion_game.screen.get_rect()
        self.settings = alien_invasion_game.settings

        # Load the ship image and get its rect.
        self.ship_path = '/home/cristiane/work/python_work/projects/'
        self.ship_path += 'alien_invasion_game/images/ship.bmp'
        self.ship_path_small = '/home/cristiane/work/python_work/projects/'
        self.ship_path_small += 'alien_invasion_game/images/ship_small.bmp'
        if size == 'small':
            self.image = pygame.image.load(self.ship_path_small)
        else:
            self.image = pygame.image.load(self.ship_path)
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

        # Store a decimal value for the ship's horizontal position.
        self.x = float(self.rect.x)

        # Movement flags
        self.moving_right = False
        self.moving_left = False
        self.is_moving = False
    
    def update(self):
        """Update the ship's position based on the movement flags."""
        # Update the ship's x value, not the rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        
        # Update rect object from self.x
        self.rect.x = self.x

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)
    
    def center_ship(self):
        """Center the ship on the screen."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)