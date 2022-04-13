# Cristiane -- 11/04/22

class GameStats:
    """Track statistics for Alien Invasion."""

    def __init__(self, alien_invasion_game):
        """Initialize statistics."""
        self.settings = alien_invasion_game.settings
        self.reset_stats()

        # Start Alien Invasion in an inactive state.
        self.game_active = False

        # High score should never be reset.
        self.high_score = 0
    
    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1