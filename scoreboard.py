# Cristiane -- 12/04/22

import pygame.font
from pygame.sprite import Group
from ship import Ship

class Scoreboard():
    """A class to report scoring information."""

    def __init__(self, alien_invasion_game):
        """Initialize scorekeeping attributes."""
        self.alien_invasion_game = alien_invasion_game
        self.screen = alien_invasion_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = alien_invasion_game.settings
        self.stats = alien_invasion_game.stats

        # Font settings for scoring information.
        self.text_color = self.settings.text_color_players
        self.font = pygame.font.SysFont(None, 30)

        self.prep_images()

    def prep_images(self):
        # Prepare the initial score image.
        self.prep_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """Turn the score into a rendered image."""
        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True,
                self.text_color, self.settings.bg_color)
        
        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 100
        self.score_rect.top = 2
    
    def prep_level(self):
        """Turn the level into a rendered image."""
        level_str = " Lvl: " + str(self.stats.level)
        self.level_image = self.font.render(level_str, True, 
                self.text_color, self.settings.bg_color)
        
        # Position the level below the score.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.left = self.score_rect.right
        self.level_rect.top = self.score_rect.top
    
    def prep_ships(self):
        """Show hoe many ships are left."""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.alien_invasion_game, 'small')
            ship.rect.x = 10 + ship_number * 30
            ship.rect.y = 2
            self.ships.add(ship)

    def show_score(self):
        """Draw scores, level, and ships to the screen."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)