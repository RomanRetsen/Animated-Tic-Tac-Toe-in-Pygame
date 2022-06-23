#test comment
#test comment
#test comment
# just addede now
# just addede now 2
# just added 4
class Stats:
    def __init__(self, g_set):
        self.g_set = g_set
        self.waiting_game_input = True
        self.drawing_click_area = False
        self.drawing_stage1_x = False
        self.drawing_stage2_x = False
        self.game_over = False
        self.gamer_turn = 'x'
        self.winningLine = None

    def switch_turns(self):
        if self.gamer_turn == 'x':
            self.gamer_turn = 'o'
        elif self.gamer_turn == 'o':
            self.gamer_turn = 'x'

    def reset_stats(self):
        self.waiting_game_input = True
        self.game_over = False
        self.gamer_turn = 'x'
        self.winningLine = None

    def setWinningLine(self):
        if self.winningLine == 'hl1':
            self.winLinex1 = self.g_set.click_area_width * 0.1
            self.winLiney1 = self.g_set.click_area_height / 2
            self.winLinex2 = self.g_set.game_screen_width - self.g_set.click_area_width * 0.1
            self.winLiney2 = self.g_set.click_area_height / 2
        elif self.winningLine == 'hl2':
            self.winLinex1 = self.g_set.click_area_width * 0.1
            self.winLiney1 = self.g_set.click_area_height + self.g_set.click_area_height / 2
            self.winLinex2 = self.g_set.game_screen_width - self.g_set.click_area_width * 0.1
            self.winLiney2 = self.g_set.click_area_height + self.g_set.click_area_height / 2
        elif self.winningLine == 'hl3':
            self.winLinex1 = self.g_set.click_area_width * 0.1
            self.winLiney1 = self.g_set.click_area_height * 2 + self.g_set.click_area_height / 2
            self.winLinex2 = self.g_set.game_screen_width - self.g_set.click_area_width * 0.1
            self.winLiney2 = self.g_set.click_area_height * 2 + self.g_set.click_area_height / 2
        elif self.winningLine == 'vl1':
            self.winLinex1 = self.g_set.click_area_width / 2
            self.winLiney1 = self.g_set.click_area_height * 0.1
            self.winLinex2 = self.g_set.click_area_width / 2
            self.winLiney2 = self.g_set.game_screen_height - self.g_set.click_area_height * 0.1
        elif self.winningLine == 'vl2':
            self.winLinex1 = self.g_set.click_area_width + self.g_set.click_area_width / 2
            self.winLiney1 = self.g_set.click_area_height * 0.1
            self.winLinex2 = self.g_set.click_area_width + self.g_set.click_area_width / 2
            self.winLiney2 = self.g_set.game_screen_height - self.g_set.click_area_height * 0.1
            pass
        elif self.winningLine == 'vl3':
            self.winLinex1 = self.g_set.click_area_width * 2 + self.g_set.click_area_width / 2
            self.winLiney1 = self.g_set.click_area_height * 0.1
            self.winLinex2 = self.g_set.click_area_width * 2 + self.g_set.click_area_width / 2
            self.winLiney2 = self.g_set.game_screen_height - self.g_set.click_area_height * 0.1
            pass
        elif self.winningLine == 'cr1':
            self.winLinex1 = self.g_set.click_area_width * 0.1
            self.winLiney1 = self.g_set.click_area_height * 0.1
            self.winLinex2 = self.g_set.game_screen_width - self.g_set.click_area_width * 0.1
            self.winLiney2 = self.g_set.game_screen_height - self.g_set.click_area_height * 0.1
            pass
        elif self.winningLine == 'cr2':
            self.winLinex1 = self.g_set.game_screen_width - self.g_set.click_area_width * 0.1
            self.winLiney1 = self.g_set.click_area_height * 0.1
            self.winLinex2 = self.g_set.click_area_width * 0.1
            self.winLiney2 = self.g_set.game_screen_height - self.g_set.click_area_height * 0.1

