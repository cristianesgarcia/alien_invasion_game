# Cristiane -- 11/04/22

import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """A class to manage bullets fired from the ship."""
    def __init__(self, alien_invasion_game):
        """Create a bullet object at the ship's current position."""
        super().__init__()
        self.screen = alien_invasion_game.screen
        self.settings = alien_invasion_game.settings
        self.color = self.settings.bullet_color

        # Create a bullet rect at (0, 0) and then set correct position.
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
            self.settings.bullet_heigh)
        self.rect.midtop = alien_invasion_game.ship.rect.midtop

        # Store the bullet's position as a decimal value.
        self.y = float(self.rect.y)
    
    def update(self):
        """Move the bullet up the screen."""
        # update the decimal position of the bullet.
        self.y -= self.settings.bullet_speed
        # Update the rect position.
        self.rect.y = self.y
    
    def draw_bullets(self):
        """Draw the bullet on the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)