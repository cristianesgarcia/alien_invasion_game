# Cristiane -- 07/04/22

import sys

import pygame

import time

from settings import Settings
from ship import Ship

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game and, and create game resources."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_heigh))
        pygame.display.set_caption("Alien Invasion.")

        self.ship = Ship(self)

        self.event = None
    
    def run_game(self):
        """Start the main loop for the game."""
        time_start = time.time()
        time_end = time.time()
        self._update_screen()
        
        while True:
            self._check_events()
            self.ship.update()
            time.sleep(0.05)
            self._update_screen()

    def _check_events(self):
        """Respond to keypress and mouse events."""
        # self.event = pygame.event.wait(self.settings.time_waiting_event)
        for event in pygame.event.get():
            self.event = event
            if self.event.type == pygame.QUIT:
                sys.exit()
            elif self.event.type == pygame.KEYDOWN:
                self._check_keydown_events()                
            elif self.event.type == pygame.KEYUP:
                self._check_keyup_events()
    
    def _check_keydown_events(self):
        """Respond to keypresses."""
        if self.event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
            self.ship.is_moving = True
        elif self.event.key == pygame.K_LEFT:
            self.ship.moving_left = True
            self.ship.is_moving = True
        elif self.event.key == pygame.K_q:
            sys.exit()
    
    def _check_keyup_events(self):
        """Respond to key releases."""
        if self.event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
            self.ship.is_moving = False
        elif self.event.key == pygame.K_LEFT:
            self.ship.moving_left = False
            self.ship.is_moving = False

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        if self.event == None or self.event.type in self.settings.redraw_events or \
            self.ship.is_moving:
            # Redraw the screen during each pass through the loop.
            self.screen.fill(self.settings.bg_color)
            self.ship.blitme()

            # Make the most recently drawn screen visible.
            pygame.display.flip()

if __name__ == '__main__':
    # Make a game instance, and run the game.
    alien_invasion_instance = AlienInvasion()
    alien_invasion_instance.run_game()

