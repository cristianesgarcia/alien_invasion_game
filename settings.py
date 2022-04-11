# Cristiane -- 08/04/22

import pygame

class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings.
        self.screen_width = 640
        self.screen_heigh = 360
        self.bg_color = (230, 230, 230)
        
        # Ship settings.
        self.ship_speed = 10

        # Redraw the screen when this events occur.
        self.redraw_events = {
            pygame.WINDOWFOCUSGAINED,
            pygame.KEYDOWN,
            pygame.KEYUP, }

        # Bullet settings.
        self.bullet_speed = 5.0
        self.bullet_width = 3
        self.bullet_heigh = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 10
