# Cristiane -- 07/04/22

import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game and, and create game resources."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_heigh))
        pygame.display.set_caption("Alien Invasion.")

        # Create an instance to store game statistics,
        #   and create a scoreboard.
        self.stats = GameStats(self)
        self.scoreboard = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        self.event = None

        # Make the play button.
        self.play_button = Button(self, "Play")
    
    def run_game(self):
        """Start the main loop for the game."""
        self._update_screen()
        
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            sleep(0.05)
            self._update_screen()
    
    def _check_events(self):
        """Respond to keypress and mouse events."""
        for event in pygame.event.get():
            self.event = event
            if self.event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            elif self.event.type == pygame.KEYDOWN:
                self._check_keydown_events()                
            elif self.event.type == pygame.KEYUP:
                self._check_keyup_events()
    
    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.start_game()

            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)

    def start_game(self):
        """Reset the game settings and statistics."""
        # Reset the game settings.
        self.settings.initialize_dynamic_settings()

        # Reset the game statistics.
        self.stats.reset_stats()
        self.stats.game_active = True
        self.scoreboard.prep_images()
        # self.scoreboard.prep_score()
        # self.scoreboard.prep_level()
        # self.scoreboard.prep_ships()

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
        elif self.event.key == pygame.K_SPACE:
            self._fire_bullet()
    
    def _check_keyup_events(self):
        """Respond to key releases."""
        if self.event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
            self.ship.is_moving = False
        elif self.event.key == pygame.K_LEFT:
            self.ship.moving_left = False
            self.ship.is_moving = False
    
    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
    
    def _update_bullets(self):
        """
        Update position of the bullets and remove the bullets that
        have disappeared.
        """
        # Update bullet positions.
        self.bullets.update()

        # Remove the bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom < 0:
                self.bullets.remove(bullet)
        
        self._check_bullet_alien_collisions()        
    
    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Remove any bullets and aliens that have collided.
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)
        
        # Update the score when collisions occur.
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.scoreboard.prep_score()
            self.scoreboard.check_high_score()

        if not self.aliens:
            self.start_new_level()
    
    def start_new_level(self):
        """Start a new level when all fleet is destroyed."""
        # Destroy existing bullets and create a new fleet.
        self.bullets.empty()
        self._create_fleet()
        self.settings.increase_speed()

        # Increase level.
        self.stats.level += 1
        self.scoreboard.prep_level()

    def _update_aliens(self):
        """
        Check if the fleet is at an edge,
        then update the positions of all aliens in the fleet.
        """
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        
        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()
    
    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 1:
            # Decrement ships_left, and update scoreboard.
            self.stats.ships_left -= 1
            self.scoreboard.prep_ships()

            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Pause
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        # if self.event == None or self.event.type in self.settings.redraw_events or \
        #     self.ship.is_moving:
        # Redraw the screen during each pass through the loop.
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()

        for bullet in self.bullets.sprites():
            bullet.draw_bullets()
        self.aliens.draw(self.screen)

        # Draw the score information.
        self.scoreboard.show_score()

        # Draw the play button if the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Make the most recently drawn screen visible.
        pygame.display.flip()
    
    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Create an alien and find the number of aliens in a row.
        # Spacing between each alien is equal to one alien width.
        alien = Alien(self)
        alien_width, alien_heigh = alien.rect.size
        available_space_x = self.settings.screen_width - 2 * alien_width
        number_aliens_x = available_space_x // (2 * alien_width)

        # Determine the number of rows of aliens that fit on the screen.
        ship_heigh = self.ship.rect.height
        available_space_y = self.settings.screen_heigh - ship_heigh
        available_space_y -= 3 * alien_heigh
        number_rows = available_space_y // (2 * alien_heigh)

        # Create the full fleet of aliens.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)
    
    def _create_alien(self, alien_number, row_number):
        """Create an alien and place it in the row."""
        alien = Alien(self)
        alien_width, alien_heigh = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)
    
    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break
    
    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_feet_direction()
                break
    
    def _change_feet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

if __name__ == '__main__':
    # Make a game instance, and run the game.
    alien_invasion_instance = AlienInvasion()
    alien_invasion_instance.run_game()

