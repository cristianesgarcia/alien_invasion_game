# Cristiane -- 12/04/22

import pygame.font

class Button:
    
    def __init__(self, alien_invasion_game, msg):
        """Initialize button attributes."""
        self.screen = alien_invasion_game.screen
        self.screen_rect = self.screen.get_rect()
        self.msg = msg

        # Set the dimensions and properties of the button.
        self.width, self.heigh = 250, 50
        self.button_color = (67, 102, 151)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Build the button's rect object using (x,y) coordinates.
        self.rect = pygame.Rect(0, 0, self.width, self.heigh)        
    
    def _prep_msg(self):
        """Turn msg into a rendered image and center text on the button."""
        self.msg_image = self.font.render(self.msg, True, self.text_color,
                self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
    
    def set_position(self, x=None, y=None):
        """
        Set the button's position in the screen.
        Center the button if x is None
        """
        if x:
            self.rect.x = x
        else:
            self.rect.center = self.screen_rect.center
        if y:
            self.rect.y = y
        else:
            self.rect.centery = self.screen_rect.centery
        
        self._prep_msg()

    def draw_button(self):
        # Draw blank button and then draw message.
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
