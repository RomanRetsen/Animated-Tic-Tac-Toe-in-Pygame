import pygame

class MessageBoard:
    def __init__(self, game_screen, g_set, g_stats):
        self.game_screen = game_screen
        self.g_set = g_set
        self.g_stats = g_stats
        self.screen_rect = game_screen.get_rect()
        self.x, self.y = 0, g_set.game_screen_height + 1
        self.width, self.height = g_set.game_screen_width, g_set.message_board_height
        self.board_color = (255, 255, 255)
        self.text_color = (0, 0, 255)
        self.font = pygame.font.SysFont(None, 25)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.prep_message("It's 'Players X' turn")

    def assignTurnMessage(self):
        if self.g_stats.gamer_turn == 'x':
            self.prep_message("It's 'Players X' turn")
        elif self.g_stats.gamer_turn == 'o':
            self.prep_message("It's 'Players O' turn")

    def gameOverMessage(self):
        print('game over message')
        if self.g_stats.gamer_turn == 'x':
            self.prep_message("Player X won. Click to reset.")
        elif self.g_stats.gamer_turn == 'o':
            self.prep_message("Player O won! Click to reset.")

    def gameOverNoWinnerMessage(self):
        self.prep_message("No one is the winner. Click to reset.")

    def prep_message(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color, self.board_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_message(self):
        self.game_screen.fill(self.board_color, self.rect)
        self.game_screen.blit(self.msg_image, self.msg_image_rect)