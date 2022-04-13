# Cristiane -- 08/04/22

import pygame

class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's static settings."""
        # Screen settings.
        self.screen_width = 640
        self.screen_heigh = 360
        self.bg_color = (230, 230, 230)
        
        # Ship settings.
        self.ship_limit = 3

        # Redraw the screen when this events occur.
        self.redraw_events = {
            pygame.WINDOWFOCUSGAINED,
            pygame.KEYDOWN,
            pygame.KEYUP, }

        # Bullet settings.
        self.bullet_width = 3
        self.bullet_heigh = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 10

        # Alien settings.
        self.fleet_drop_speed = 10
        
        # How quickly the game speeds up
        self.speedup_scale = 1

        # How quickly the alien points values increase
        self.score_scale = 1.5

        self.initialize_dynamic_settings()
    
    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed = 10
        self.bullet_speed = 5.0
        self.alien_speed = 2.0

        # Fleet direction of 1 represents right, -1 represents left.
        self.fleet_direction = 1

        # Scoring
        self.alien_points = 50

    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.ship_speed += self.speedup_scale
        self.bullet_speed += self.speedup_scale
        self.alien_speed += self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)