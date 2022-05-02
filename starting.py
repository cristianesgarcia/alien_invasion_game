# Cristiane -- 18/04/22

import pygame
import json
from os.path import exists

from game_state import GameState
from button import Button
import running
import create_players_file

class Starting(GameState):
    """A class to represent the Starting state."""

    def __init__(self, game):
        """Initialize the class attributes."""
        self.game = game
        self.screen = self.game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = game.settings
        self.player_name = self.game.get_player_name()

        # Store the scoring information.
        self.file_path = 'players.json'

        # Font settings.
        self.font = pygame.font.SysFont(None, 25)
        self.font_title = pygame.font.SysFont(None, 40)

        # Create a file to store score information.
        self._create_players_file()

        # Load the score information from the file.
        self._get_players()

        # Prepare the images.
        self._prep_images()
    
    def _create_players_file(self):
        """Create a file to store the scores, if it does not exist."""
        if not exists(self.file_path):
            create_players_file.create_file()
    
    def _get_players(self):
        """Get the players score stored in a json file."""
        with open(self.file_path) as f:
            self.list_players = json.load(f)
            
    def _prep_images(self):
        """Images composing the screen."""
        self._prep_title()
        self._prep_subtitle()
        self._prep_players()
        self._prep_name()
        self._prep_play_button()

    def _prep_title(self):
        """Turn the title into a rendered image."""
        self.title_image = self.font_title.render(self.settings.title_txt, True,
            self.settings.text_color_title, self.settings.bg_color)

        # Display the title at the top center of the screen.
        self.title_rect = self.title_image.get_rect()
        self.title_rect.center = self.screen_rect.center
        self.title_rect.top = self.settings.space_on_top
    
    def _prep_subtitle(self):
        """Turn the subtitle information into a rendered image."""
        self.subtitle_image = self.font.render(self.settings.subtitle_txt, True,
                self.settings.text_color_players, self.settings.bg_color)
        
        self.subtitle_rect = self.subtitle_image.get_rect()
        self.subtitle_rect.center = self.title_rect.center
        self.subtitle_rect.top = self.title_rect.bottom + self.settings.space_on_top
    
    def _prep_players(self):
        """Turn the list of players into a rendered image."""
        self.players = {}

        for item in range(len(self.list_players)):
            player = self.list_players[item]
            identification = f"{str(player['nickname'])} "
            separator = self.settings.separator*self.settings.size_separator
            identification += f"{separator}"
            if str(player['points']) == '--':
                identification += f" {str(player['points'])}"
            else:
                identification += " {:,}".format((player['points']))
            players_image = self.font.render(identification, True,
                self.settings.text_color_players, self.settings.bg_color)
            players_rect = players_image.get_rect()
            players_rect.center = self.screen_rect.center
            players_rect.top = self.subtitle_rect.top
            players_rect.top += (item+1)*self.settings.space_in_lines
            self.players[players_image] = players_rect
    
    def _prep_name(self):
        """
        Create a label and a input box to receive the player's name.
        """
        last_rect_position = list(self.players.values())
        last_rect_position = last_rect_position[-1]
        self.label_name_image = self.font.render('Your name:', True, 
            self.settings.text_color_title, self.settings.bg_color)
        self.label_name_rect = self.label_name_image.get_rect()
        self.label_name_rect.x = last_rect_position.x
        self.label_name_rect.y = last_rect_position.bottom
        self.label_name_rect.y += self.settings.space_in_lines

        self.name_image = self.font.render(self.player_name, True, 
            self.settings.text_color_title, self.settings.bg_color)
        self.name_rect = self.name_image.get_rect()
        self.name_rect.x = self.label_name_rect.right + 10
        self.name_rect.y = self.label_name_rect.y
    
    def _prep_play_button(self):
        """Create the play button."""
        self.play_button = Button(self, "Play")
        self.play_button.set_position(None,
            self.label_name_rect.bottom + self.settings.space_in_lines)
    
    def _draw_name(self, player_name):
        """Redraw only the player's name box."""
        self.name_image = self.font.render(str(player_name), True, 
            self.settings.text_color_title, self.settings.bg_color)

    def _draw_screen(self):
        """Draw the screen."""
        self.screen.fill(self.settings.bg_color)
        self.screen.fill(self.settings.bg_color, self.title_rect)
        self.screen.fill(self.settings.bg_color, self.subtitle_rect)
        self.screen.fill(self.settings.bg_color, self.label_name_rect)
        self.screen.fill(self.settings.bg_color, self.name_rect)
        self.screen.blit(self.title_image, self.title_rect)
        self.screen.blit(self.subtitle_image, self.subtitle_rect)
        self.screen.blit(self.label_name_image, self.label_name_rect)
        self.screen.blit(self.name_image, self.name_rect)

        for key, value in self.players.items():
            self.screen.fill(self.settings.bg_color, value)
            self.screen.blit(key, value)
        
        self.play_button.draw_button()
    
    def on_click(self, mouse_pos):
        """Respond to clicks with the mouse right button."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked:
            self.game.set_current_state(running.Running(self.game))
            self.game.set_player_name(self.player_name)
    
    def on_key_down(self, event):
        """Store the player's name."""
        self.player_name = self.game.get_player_name().replace('|', '')
        if event.key == pygame.K_BACKSPACE:
            self.player_name = self.player_name[:-1]
        else:
            self.player_name += event.unicode
        self.game.set_player_name(self.player_name)
        self._draw_name(self.player_name)
        self.update_screen()
    
    def on_key_up(self, event):
        """Does nothing."""
        pass

    def update_screen(self):
        """Draw the screen."""
        self._draw_screen()
        pygame.display.flip()

    def update_players(self, current_player):
        """Update the json file with the top five players."""
        players = self.list_players.copy()
        for item in range(len(self.list_players)):
            player = self.list_players[item]
            if (player['points'] == '--' or
                int(current_player['points']) > int(player['points'])):
                players.insert(item, current_player)
                break
            elif int(current_player['points']) == int(player['points']):
                players.insert(item + 1, current_player)
                break
        self.list_players = players[0:5]
        with open(self.file_path, 'w') as f:
            json.dump(self.list_players, f)
        self._prep_players()
        self.update_screen()
