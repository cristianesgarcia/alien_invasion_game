# Cristiane -- 18/04/22

import pygame

from starting import Starting
from settings import Settings

class Game:
    """Class to manage the game events."""

    def __init__(self):
        """Initialize the class."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_heigh))
        pygame.display.set_caption("Alien Invasion")

        self.player_name = '|'

        self.currentState = Starting(self)
    
    def set_current_state(self, state):
        """Update the current state."""
        self.currentState = state
    
    def get_player_name(self):
        """Return the player's name."""
        return self.player_name
    
    def set_player_name(self, player_name):
        """Update the player's name."""
        self.player_name = player_name
    
    def on_click(self, mouse_pos):
        """Respond to a click event."""
        self.currentState.on_click(mouse_pos)
    
    def on_key_down(self, event):
        """Respond to a keydown event."""
        self.currentState.on_key_down(event)
    
    def on_key_up(self, event):
        """Respond to a keyup event."""
        self.currentState.on_key_up(event)
    
    def update_screen(self):
        """Draw the screen."""
        self.currentState.update_screen()
    
    def update_players(self, current_player):
        """Does nothing."""
        pass
    