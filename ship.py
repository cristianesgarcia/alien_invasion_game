# Cristiane -- 08/04/22

import pygame

class Ship:
    """A class to manage the ship."""

    def __init__(self, alien_invasion_game):
        """Initialize the ship and set its start position."""
        self.screen = alien_invasion_game.screen
        self.screen_rect = alien_invasion_game.screen.get_rect()

        # Load the ship image and get its rect.
        self.ship_path = '/home/cristiane/work/python_work/projects/'
        self.ship_path += 'alien_invasion_game/images/ship.bmp'
        self.image = pygame.image.load(self.ship_path)
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)