# Cristiane -- 15/04/22

import pygame.font
from input_box import InputBox
from button import Button

class ScoreScreen():
    """A class to report the top five players and to start the game."""

    def __init__(self, alien_invasion_game):
        self.screen = alien_invasion_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = alien_invasion_game.settings

        # Font settings.
        self.text_color_players = (30, 30, 30)
        self.text_color_title = (237, 11, 11) # red
        self.font = pygame.font.SysFont(None, 25)
        self.font_title = pygame.font.SysFont(None, 40)

        # Texts to be displayed.
        self.title_txt = "Scores"
        self.size_separator_txt = 30
        self.separator_txt = '.'
        self.space_txt = 30
        self.space_top_txt = 10
        self.subtitle_txt = "Player "
        self.subtitle_txt += f"{self.separator_txt*self.size_separator_txt}"
        self.subtitle_txt += " Points"

        # Create an input box
        self.input_box = InputBox(alien_invasion_game, 
            self.screen_rect.centerx, self.screen_rect.centery + 60,
            200, 30, 'Your name')

        self.play_button = Button(alien_invasion_game, "Play",
            200, self.screen_rect.bottom - 60)

        # TODO: LOAD THE TOP 5 PLAYERS FROM A FILE
        self.list_players = [
            {'pos':1, 'nickname':'player1', 'points':20000, 'level':20},
            {'pos':2, 'nickname':'player2', 'points':18000, 'level':15},
            {'pos':3, 'nickname':'player3', 'points':7000, 'level':10},
            {'pos':4, 'nickname':'player4', 'points':5320, 'level':5},
            {'pos':5, 'nickname':'player5', 'points':1000, 'level':2},
            ]

        self.prep_title()
        self.prep_subtitle()
        self.prep_players()
    
    def prep_title(self):
        """Turn the title into a rendered image."""
        self.title_image = self.font_title.render(self.title_txt, True,
            self.text_color_title, self.settings.bg_color)

        # Display the title at the top center of the screen.
        self.title_rect = self.title_image.get_rect()
        self.title_rect.center = self.screen_rect.center
        self.title_rect.top = self.space_top_txt
    
    def prep_subtitle(self):
        """Turn the subtitle information into a rendered image."""
        self.subtitle_image = self.font.render(self.subtitle_txt, True,
                self.text_color_players, self.settings.bg_color)
        
        self.subtitle_rect = self.subtitle_image.get_rect()
        self.subtitle_rect.center = self.title_rect.center
        self.subtitle_rect.top = self.title_rect.bottom + self.space_top_txt
    
    def prep_players(self):
        """Turn the list of players into a rendered image."""
        self.players = {}

        for item in self.list_players:
            identification = f"{str(item['nickname'])} "
            identification += f"{self.separator_txt*self.size_separator_txt}"
            identification += f" {str(item['points'])}"
            players_image = self.font.render(identification, True,
                self.text_color_players, self.settings.bg_color)
            players_rect = players_image.get_rect()
            players_rect.center = self.screen_rect.center
            players_rect.top = self.subtitle_rect.top
            players_rect.top += item['pos']*self.space_txt
            self.players[players_image] = players_rect

    def prep_input_box(self):
        """Draw an input box to collect the current player's name."""

    def draw_score_screen(self):
        """Draw the screen."""
        self.screen.fill(self.settings.bg_color)
        self.screen.fill(self.settings.bg_color, self.title_rect)
        self.screen.fill(self.settings.bg_color, self.subtitle_rect)
        self.screen.blit(self.title_image, self.title_rect)
        self.screen.blit(self.subtitle_image, self.subtitle_rect)

        for key, value in self.players.items():
            self.screen.fill(self.settings.bg_color, value)
            self.screen.blit(key, value)
        
        self.input_box.draw_input_box()
        self.play_button.draw_button()