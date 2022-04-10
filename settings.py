# Cristiane -- 08/04/22

import pygame

class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        self.screen_width = 1200
        self.screen_heigh = 600
        self.bg_color = (230, 230, 230)
        self.time_waiting_event = 100
        self.ship_speed = 1.5
        self.redraw_events = {pygame.WINDOWFOCUSGAINED,
            pygame.KEYDOWN, pygame.KEYUP}
