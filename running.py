# Cristiane -- 19/04/22

import pygame
from time import sleep

from game_state import GameState
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
import starting

class Running(GameState):
    """A class to represent the Running state."""

    def __init__(self, game):
        """Initialize the class attributes."""
        self.game = game
        self.screen = self.game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = game.settings

        # Initialize the game in active mode.
        self.active = True
        self.pause_button = Button(self, 'Game paused')
        self.pause_button.set_position()

        # Font settings.
        self.font = pygame.font.SysFont(None, 25)
        self.font_title = pygame.font.SysFont(None, 40)

        # Initialize the game.
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.stats = GameStats(self)
        self.scoreboard = Scoreboard(self)

        self._start_game()
    
    def _start_game(self):
        """Reset the game settings and statistics."""
        # Reset the game settings.
        self.settings.initialize_dynamic_settings()

        # Reset the game statistics.
        self.stats.reset_stats()
        self.scoreboard.prep_images()
        self._create_fleet()
        pygame.mouse.set_visible(False)
    
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
            starting_state = starting.Starting(self.game)
            self.game.set_current_state(starting_state)
            current_player = {'nickname':self.game.get_player_name(),
                'points':self.stats.score,
                'level':self.stats.level}
            starting_state.update_players(current_player)
            pygame.mouse.set_visible(True)
    
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

        if not self.aliens:
            self._start_new_level()
    
    def _start_new_level(self):
        """Start a new level when all fleet is destroyed."""
        # Destroy existing bullets and create a new fleet.
        self.bullets.empty()
        self._create_fleet()
        self.settings.increase_speed()

        # Increase level.
        self.stats.level += 1
        self.scoreboard.prep_level()

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _pause_resume_game(self):
        """Pause/resume the game."""
        if self.active:
            self.active = False
            pygame.mouse.set_visible(True)
        else:
            self.active = True
            pygame.mouse.set_visible(False)
    
    def on_click(self, mouse_pos):
        """Does nothing."""
        pass

    def on_key_down(self, event):
        """Respond to keypresses."""
        if self.active:
            if event.key == pygame.K_RIGHT:
                self.ship.moving_right = True
                self.ship.is_moving = True
            elif event.key == pygame.K_LEFT:
                self.ship.moving_left = True
                self.ship.is_moving = True
            elif event.key == pygame.K_SPACE:
                self._fire_bullet()
        
        if event.key == pygame.K_ESCAPE:
            self._pause_resume_game()

    def on_key_up(self, event):
        """Respond to key releases."""
        if self.active:
            if event.key == pygame.K_RIGHT:
                self.ship.moving_right = False
                self.ship.is_moving = False
            elif event.key == pygame.K_LEFT:
                self.ship.moving_left = False
                self.ship.is_moving = False

    def update_screen(self):
        """Draw the respective screen (game active or paused)."""
        if self.active:
            self.ship.update()
            self._update_bullets()
            self._update_aliens()

            self.screen.fill(self.settings.bg_color)
            self.ship.blitme()
            for bullet in self.bullets.sprites():
                bullet.draw_bullets()
            self.aliens.draw(self.screen)

            # Draw the score information.
            self.scoreboard.show_score()
        else:
            self.pause_button.draw_button()
        
        pygame.display.flip()
    
    def update_players(self, current_player):
        """Does nothing."""
        pass

