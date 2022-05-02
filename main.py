# Cristiane -- 18/04/22

import pygame
import sys
from time import sleep

from game import Game

class Main():
    """Overall class to manage the assets and behavior of the game."""

    def __init__(self):
        """Initialize the game."""
        self.game = Game()
    
    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()

            sleep(0.05)
            self.game.update_screen()
    
    def _check_events(self):
        """Respond to keypress and mouse events."""
        for event in pygame.event.get():
            self.event = event
            if self.event.type == pygame.QUIT:
                sys.exit()
            elif (event.type == pygame.MOUSEBUTTONDOWN and 
                    event.button == pygame.BUTTON_LEFT):
                self.game.on_click(pygame.mouse.get_pos())
            elif event.type == pygame.KEYDOWN:
                self.game.on_key_down(event)
            elif event.type == pygame.KEYUP:
                self.game.on_key_up(event)

if __name__ == '__main__':
    # Make a game instance, and run the game.
    main_instance = Main()
    main_instance.run_game()